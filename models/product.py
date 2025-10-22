from beanie import Document
from typing import Optional

class Product(Document):
    name: str
    description: Optional[str] = None
    price: float
    in_stock: int = 0