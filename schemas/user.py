from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId
from schemas.common import PyObjectId


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    password: str


class UserRead(BaseModel):
    id: PyObjectId = Field(alias="_id")
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True

    class Config:
        populate_by_name = True  
        arbitrary_types_allowed = True  
        json_encoders = {ObjectId: str} 


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
