from beanie import Document, PydanticObjectId
from pydantic import Field
from typing import Optional

class Product(Document):

    name: str = Field(..., index=True)
    description: str
    price: float = Field(..., ge=0) 
    inventory: int = Field(..., ge=0) 

    class Settings:
        name = "products"
