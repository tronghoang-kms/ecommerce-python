from fastapi import Depends, HTTPException, status
from models.user import User
from models.cart import Cart
from schemas.cart import CartItemCreate, CartDetail, CartItemRead
from schemas.product import ProductRead
from repositories.cart_repository import CartRepository, get_cart_repository
from repositories.product_repository import ProductRepository, get_product_repository
from beanie import PydanticObjectId
from bson import ObjectId
from bson.dbref import DBRef

class CartService:

    def __init__(
        self,
        cart_repo: CartRepository = Depends(get_cart_repository),
        product_repo: ProductRepository = Depends(get_product_repository)
    ):
        self.cart_repo = cart_repo
        self.product_repo = product_repo

    async def _get_cart_details(self, cart: Cart) -> CartDetail:
        total_price = 0
        items_read = []

        ref_map = {}  
        ref_ids = []  
        embedded = {}  

        for idx, item in enumerate(cart.items):
            prod = item.product
            if hasattr(prod, "price") or (isinstance(prod, dict) and "price" in prod):
                embedded[idx] = prod
                continue

            pid = None
            if isinstance(prod, DBRef):
                pid = prod.id
            elif isinstance(prod, (PydanticObjectId, ObjectId)):
                pid = prod
            else:
                pid = getattr(prod, "id", None) or (str(prod) if prod is not None else None)

            if pid is not None:
                ref_map[idx] = pid
                ref_ids.append(pid)

        # Batch fetch referenced products
        fetched = {}
        if ref_ids:
            prods = await self.product_repo.get_by_ids(ref_ids)
            for p in prods:
                key = None
                if getattr(p, "id", None) is not None:
                    key = str(p.id)
                elif getattr(p, "_id", None) is not None:
                    key = str(p._id)
                else:
                    key = str(getattr(p, "pk", None))
                fetched[key] = p

        # Build result list using embedded or fetched products
        for idx, item in enumerate(cart.items):
            product_obj = None
            if idx in embedded:
                product_obj = embedded[idx]
            elif idx in ref_map:
                pid = ref_map[idx]
                product_obj = fetched.get(str(pid))

            if product_obj is None:
                # product missing; skip
                continue

            product_data = ProductRead.model_validate(product_obj)
            items_read.append(CartItemRead(product=product_data, quantity=item.quantity))
            total_price += product_obj.price * item.quantity

        return CartDetail(items=items_read, total_price=total_price)


    async def get_user_cart(self, user: User) -> CartDetail:
        cart = await self.cart_repo.get_or_create_cart(user)
        return await self._get_cart_details(cart)

    async def add_item_to_cart(self, user: User, item_create: CartItemCreate) -> CartDetail:
        product = await self.product_repo.get_by_id(item_create.product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
            
        if product.inventory < item_create.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough product in stock")
            
        cart = await self.cart_repo.get_or_create_cart(user)
        
        cart = await self.cart_repo.add_or_update_item(cart, product, item_create.quantity)
        
        return await self._get_cart_details(cart)
        
    async def remove_item_from_cart(self, user: User, product_id: PydanticObjectId) -> CartDetail:
        cart = await self.cart_repo.get_cart_by_user(user)
        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
            
        cart = await self.cart_repo.remove_item(cart, str(product_id))
        
        return await self._get_cart_details(cart)


def get_cart_service() -> CartService:
    return CartService(
        cart_repo=get_cart_repository(),
        product_repo=get_product_repository()
    )
