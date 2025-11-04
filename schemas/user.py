from pydantic import BaseModel, EmailStr, Field
from beanie import PydanticObjectId
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
     password: str = Field(
        ..., 
        min_length=8, 
        max_length=72, 
        description="Password must be between 8 and 72 characters"
    )

class UserRead(UserBase):
    id: PydanticObjectId
    is_admin: bool

    class Config:
        from_attributes = True
