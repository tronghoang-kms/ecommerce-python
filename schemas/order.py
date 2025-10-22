from pydantic import BaseModel
from typing import List, Optional


class OrderCreate(BaseModel):
    user_id: str                  
    product_ids: List[str]        


class OrderUpdate(BaseModel):
    user_id: Optional[str] = None       
    product_ids: Optional[List[str]] = None  
    status: Optional[str] = None        


class OrderRead(BaseModel):
    id: str
    user_id: str
    product_ids: List[str]
    total_amount: float
    status: str