from beanie import Document
from datetime import datetime
from pydantic import Field, EmailStr

class User(Document):
    email: EmailStr
    password: str
    full_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"