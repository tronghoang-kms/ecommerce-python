from models.order import Order, OrderItemSchema
from models.user import User
from typing import List

class OrderRepository:

    async def create_order(self, user: User, items: List[OrderItemSchema], total_price: float, stripe_session_id: str) -> Order:
        order = Order(
            user=user, 
            items=items,
            total_price=total_price,
            stripe_session_id=stripe_session_id,
            status="pending" # Sẽ cập nhật thành 'paid' bởi webhook
        )
        await order.create()
        return order
        
    async def get_order_by_stripe_session(self, session_id: str) -> Order | None:
        return await Order.find_one(Order.stripe_session_id == session_id)

    async def update_order_status(self, order: Order, new_status: str) -> Order:
        order.status = new_status
        await order.save()
        return order
        

# Dependency function để inject
def get_order_repository() -> OrderRepository:
    return OrderRepository()
