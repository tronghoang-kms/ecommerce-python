from models.product import Product
from schemas.product import ProductCreate, ProductUpdate
from beanie import PydanticObjectId
from typing import List, Optional
from beanie.operators import RegEx

class ProductRepository:

    async def get_by_id(self, product_id: PydanticObjectId) -> Optional[Product]:

        return await Product.get(product_id)

    async def get_by_ids(self, product_ids: List[PydanticObjectId]) -> List[Product]:
        normalized = []
        for pid in product_ids:
            try:
                normalized.append(PydanticObjectId(pid))
            except Exception:
                normalized.append(pid)

        return await Product.find({"_id": {"$in": normalized}}).to_list()

    async def get_all_products(self, search: Optional[str] = None) -> List[Product]:

        if search:

            search_regex = RegEx("name", search, "i")
            return await Product.find(search_regex).to_list()
        return await Product.find_all().to_list()

    async def create_product(self, product_create: ProductCreate) -> Product:

        product = Product(**product_create.model_dump())
        await product.create()
        return product

    async def update_product(self, product_id: PydanticObjectId, product_update: ProductUpdate) -> Optional[Product]:

        product = await self.get_by_id(product_id)
        if not product:
            return None
        

        update_data = product_update.model_dump(exclude_unset=True)
        if update_data:
            await product.update({"$set": update_data})

            product = await Product.get(product.id)
        return product

    async def delete_product(self, product_id: PydanticObjectId) -> bool:

        product = await self.get_by_id(product_id)
        if product:
            await product.delete()
            return True
        return False
    
    async def update_product_inventory(self, product_id: PydanticObjectId, quantity_change: int) -> Optional[Product]:

        product = await self.get_by_id(product_id)
        if not product:
            return None
        
        if product.inventory + quantity_change < 0:

            return None 

        product.inventory += quantity_change
        await product.save()
        return product


def get_product_repository() -> ProductRepository:
    return ProductRepository()
