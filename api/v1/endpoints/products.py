from fastapi import APIRouter, Depends, status
from schemas.product import ProductCreate, ProductRead, ProductUpdate
from services.product_service import ProductService, get_product_service
from models.user import User
from security.auth import get_current_admin_user, get_current_user
from beanie import PydanticObjectId
from typing import List, Optional

router = APIRouter()



@router.get("/", response_model=List[ProductRead])
async def list_products(
    search: Optional[str] = None,
    product_service: ProductService = Depends(get_product_service)
):

    return await product_service.get_all(search)

@router.get("/{product_id}", response_model=ProductRead)
async def get_product_detail(
    product_id: PydanticObjectId,
    product_service: ProductService = Depends(get_product_service)
):

    return await product_service.get_by_id(product_id)


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductCreate,
    admin_user: User = Depends(get_current_admin_user),
    product_service: ProductService = Depends(get_product_service)
):
    return await product_service.create(product_in)

@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: PydanticObjectId,
    product_in: ProductUpdate,
    admin_user: User = Depends(get_current_admin_user),
    product_service: ProductService = Depends(get_product_service)
):
    return await product_service.update(product_id, product_in)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: PydanticObjectId,
    admin_user: User = Depends(get_current_admin_user),
    product_service: ProductService = Depends(get_product_service)
):
    """
    [Admin] Xóa sản phẩm.
    """
    await product_service.delete(product_id)
    return None # Trả về 204
