from models.user import User
from schemas.user import UserCreate
from security.auth import get_password_hash
from pydantic import EmailStr
from typing import Optional

class UserRepository:
    
    async def get_user_by_email(self, email: EmailStr) -> Optional[User]:

        return await User.find_one(User.email == email)

    async def create_user(self, email: EmailStr, hashed_password: str, is_admin: bool) -> User:
        
        user = User(
            email=email,
            hashed_password=hashed_password,
            is_admin=is_admin
        )
        await user.create()
        return user

# Dependency function để inject
def get_user_repository() -> UserRepository:
    return UserRepository()
