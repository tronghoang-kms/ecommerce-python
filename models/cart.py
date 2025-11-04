from beanie import Document, Link, PydanticObjectId
from pydantic import Field, BaseModel
from typing import List
from models.user import User

class CartItemSchema(BaseModel):
    product: PydanticObjectId
    quantity: int = Field(..., gt=0)

class Cart(Document):
    user: Link[User] = Field(..., unique=True)
    items: List[CartItemSchema] = Field(default_factory=list)

    class Settings:
        name = "carts"
