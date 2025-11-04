import datetime
from beanie import Document, Link, PydanticObjectId
from pydantic import Field, BaseModel
from typing import List, Optional
from models.user import User

class OrderItemSchema(BaseModel):
    product_id: PydanticObjectId
    product_name: str
    price_at_purchase: float
    quantity: int

class Order(Document):

    user: Link[User]
    items: List[OrderItemSchema] = Field(default_factory=list)
    total_price: float
    status: str = Field(default="pending") # (pending, paid, shipped, cancelled)
    stripe_session_id: Optional[str] = Field(default=None, index=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    class Settings:
        name = "orders"
