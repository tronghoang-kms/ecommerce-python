from beanie import Document
from pydantic import EmailStr, Field

class User(Document):
    email: EmailStr = Field(..., unique=True, index=True)
    hashed_password: str
    is_admin: bool = Field(default=False)

    class Settings:
        name = "users"
