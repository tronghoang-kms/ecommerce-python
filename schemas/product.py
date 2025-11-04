from pydantic import BaseModel
from beanie import PydanticObjectId
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    inventory: int

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: PydanticObjectId

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    inventory: Optional[int] = None
