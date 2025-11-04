from fastapi import Depends, HTTPException, status
from repositories.product_repository import ProductRepository, get_product_repository
from schemas.product import ProductCreate, ProductUpdate
from models.product import Product
from beanie import PydanticObjectId
from typing import List, Optional

class ProductService:

    def __init__(self, product_repo: ProductRepository = Depends(get_product_repository)):
        self.product_repo = product_repo

    async def get_all(self, search: Optional[str] = None) -> List[Product]:

        return await self.product_repo.get_all_products(search)

    async def get_by_id(self, product_id: PydanticObjectId) -> Product:

        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return product

    async def create(self, product_create: ProductCreate) -> Product:
        return await self.product_repo.create_product(product_create)

    async def update(self, product_id: PydanticObjectId, product_update: ProductUpdate) -> Product:
        product = await self.product_repo.update_product(product_id, product_update)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return product

    async def delete(self, product_id: PydanticObjectId) -> dict:
        deleted = await self.product_repo.delete_product(product_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return {"message": "Product deleted successfully"}


def get_product_service() -> ProductService:
    return ProductService(product_repo=get_product_repository())
