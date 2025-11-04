from fastapi import APIRouter
from api.v1.endpoints import auth, users, products, cart, checkout

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["1. Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["2. Users"])
api_router.include_router(products.router, prefix="/products", tags=["3. Products"])
api_router.include_router(cart.router, prefix="/cart", tags=["4. Cart"])
api_router.include_router(checkout.router, prefix="/checkout", tags=["5. Checkout & Payment"])
