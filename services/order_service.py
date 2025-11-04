from fastapi import Depends, HTTPException, status
from models.user import User
from models.order import Order, OrderItemSchema
from repositories.order_repository import OrderRepository, get_order_repository
from repositories.cart_repository import CartRepository, get_cart_repository
from repositories.product_repository import ProductRepository, get_product_repository
import stripe
from core.config import settings

class OrderService:

    def __init__(
        self,
        order_repo: OrderRepository = Depends(get_order_repository),
        cart_repo: CartRepository = Depends(get_cart_repository),
        product_repo: ProductRepository = Depends(get_product_repository)
    ):
        self.order_repo = order_repo
        self.cart_repo = cart_repo
        self.product_repo = product_repo

    async def create_order_from_stripe_session(self, session: stripe.checkout.Session) -> Order:
        """
        Tạo đơn hàng sau khi Stripe session hoàn thành (được gọi từ webhook).
        Đây là một logic quan trọng:
        1. Lấy thông tin giỏ hàng từ User ID (lưu trong metadata)
        2. Tạo Order
        3. Giảm tồn kho sản phẩm
        4. Xóa giỏ hàng
        """
        user_id = session.metadata.get("user_id")
        if not user_id:
            raise ValueError("User ID not found in Stripe session metadata")

        # 1. Lấy giỏ hàng
        # Tạm thời chúng ta phải tìm user, rồi tìm giỏ hàng
        # Đây là một điểm yếu khi service này không có `User` object
        # Cách tốt hơn là `Webhook` endpoint sẽ tìm user trước
        # Nhưng để đơn giản, chúng ta giả định webhook endpoint sẽ cung cấp user_id
        
        # Giả sử chúng ta có thể lấy User từ user_id (cần 1 hàm repo)
        # user = await user_repo.get_by_id(user_id) # Cần thêm hàm này
        # cart = await self.cart_repo.get_cart_by_user(user)
        
        # Lấy giỏ hàng (cần sửa lại repo để tìm bằng user_id)
        # Tạm thời, chúng ta sẽ tạo Order dựa trên line_items của Stripe
        # (Đây là cách an toàn hơn, vì giỏ hàng có thể đã thay đổi)
        
        # Stripe API trả về danh sách line items
        stripe.api_key = settings.STRIPE_SECRET_KEY
        line_items = stripe.checkout.Session.list_line_items(session.id, limit=50)

        order_items = []
        total_price = 0
        
        # Chúng ta cần map line_items từ Stripe về product_id của chúng ta
        # Đây là một phần phức tạp. Khi tạo checkout session,
        # chúng ta nên lưu product_id vào metadata của price_data.
        
        # ---
        # GIẢ ĐỊNH ĐƠN GIẢN HÓA:
        # Thay vì dựa vào line_items của Stripe, chúng ta sẽ dựa vào
        # giỏ hàng của user tại thời điểm ngay trước khi checkout.
        # Webhook sẽ tạo Order, giảm tồn kho, và xóa giỏ hàng.
        
        # Lấy lại order nếu nó đã được tạo (để tránh xử lý webhook 2 lần)
        existing_order = await self.order_repo.get_order_by_stripe_session(session.id)
        if existing_order:
            return existing_order # Đã xử lý

        cart = await self.cart_repo.get_cart_by_user(User(id=user_id)) # type: ignore
        if not cart or not cart.items:
            raise ValueError("Cart is empty or not found")
            
        await cart.fetch_all_links() 
        
        order_items_schema = []
        total_price = 0
        

        for item in cart.items:
            product = item.product
            if product.inventory < item.quantity:
                raise Exception(f"Product {product.name} is out of stock.")
            
            await self.product_repo.update_product_inventory(product.id, -item.quantity)
            
            order_items_schema.append(
                OrderItemSchema(
                    product_id=product.id,
                    product_name=product.name,
                    price_at_purchase=product.price,
                    quantity=item.quantity
                )
            )
            total_price += product.price * item.quantity
            
        order = await self.order_repo.create_order(
            user=cart.user, # type: ignore
            items=order_items_schema,
            total_price=total_price,
            stripe_session_id=session.id
        )
        

        await self.order_repo.update_order_status(order, "paid")
        
        await self.cart_repo.clear_cart(cart)
        
        return order


def get_order_service() -> OrderService:
    return OrderService(
        order_repo=get_order_repository(),
        cart_repo=get_cart_repository(),
        product_repo=get_product_repository()
    )
