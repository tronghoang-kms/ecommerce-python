from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    in_stock: int = 0

class ProductRead(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    price: float
    in_stock: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[int] = None