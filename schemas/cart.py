from pydantic import BaseModel, Field
from beanie import PydanticObjectId
from typing import List, Optional
from schemas.product import ProductRead

class CartItemCreate(BaseModel):
    product_id: PydanticObjectId
    quantity: int = Field(1, gt=0)

class CartItemRead(BaseModel):
    product: ProductRead
    quantity: int

    class Config:
        from_attributes = True

class CartDetail(BaseModel):
    items: List[CartItemRead]
    total_price: float
