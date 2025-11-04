from fastapi import APIRouter, Depends, status
from schemas.cart import CartDetail, CartItemCreate
from models.user import User
from security.auth import get_current_user
from services.cart_service import CartService, get_cart_service
from beanie import PydanticObjectId

router = APIRouter()

@router.get("/", response_model=CartDetail)
async def get_user_cart(
    current_user: User = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service)
):

    return await cart_service.get_user_cart(current_user)

@router.post("/items", response_model=CartDetail)
async def add_item_to_cart(
    item_in: CartItemCreate,
    current_user: User = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service)
):

    return await cart_service.add_item_to_cart(current_user, item_in)

@router.delete("/items/{product_id}", response_model=CartDetail)
async def remove_item_from_cart(
    product_id: PydanticObjectId,
    current_user: User = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service)
):

    return await cart_service.remove_item_from_cart(current_user, product_id)
