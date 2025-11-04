from models.cart import Cart, CartItemSchema
from models.user import User
from models.product import Product

from typing import Optional

class CartRepository:

    async def get_cart_by_user(self, user: User) -> Optional[Cart]:
        cart = await Cart.find_one({"user": user.id})
        if not cart:
            cart = await Cart.find_one({"user.$id": user.id})

        if cart:
            cart.user = user  # type: ignore
        return cart

    async def get_or_create_cart(self, user: User) -> Cart:
        cart = await self.get_cart_by_user(user)
        if not cart:
            cart = Cart(user=user) # type: ignore
            await cart.create()
        return cart

    async def add_or_update_item(self, cart: Cart, product: Product, quantity: int) -> Cart:
        # Compare stored product id with the incoming product id.
        existing_item = next((item for item in cart.items if str(item.product) == str(product.id)), None)

        if existing_item:
            existing_item.quantity = quantity
        else:
            # Store the product id (PydanticObjectId) in the cart item.
            new_item = CartItemSchema(product=product.id, quantity=quantity)
            cart.items.append(new_item)
            
        await cart.save()
        return cart

    async def remove_item(self, cart: Cart, product_id: str) -> Cart:
 
        cart.items = [item for item in cart.items if str(item.product) != product_id]
        await cart.save()
        return cart

    async def clear_cart(self, cart: Cart) -> Cart:
 
        cart.items = []
        await cart.save()
        return cart

# Dependency function để inject
def get_cart_repository() -> CartRepository:
    return CartRepository()
