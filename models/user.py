from beanie import Document
from pydantic import EmailStr
from typing import Optional

class User(Document):
    username: str
    email: EmailStr
    is_active: bool = True
    full_name: Optional[str] = None