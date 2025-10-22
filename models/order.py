from beanie import Document, Link
from typing import List
from models.user import User
from models.product import Product

class Order(Document):
    user: Link[User]
    products: List[Link[Product]]
    total_amount: float
    status: str = "pending"