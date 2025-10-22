
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    password: str 


class UserRead(BaseModel):
    id: str
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
