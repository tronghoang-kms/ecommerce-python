from fastapi import Depends, HTTPException, status
from pydantic import EmailStr
from typing import Optional
from models.user import User
from schemas.user import UserCreate
from repositories.user_repository import UserRepository, get_user_repository
from security.auth import verify_password, create_access_token, get_password_hash


class AuthService:
    
    def __init__(self, user_repo: UserRepository = Depends(get_user_repository)):
        self.user_repo = user_repo

    async def _register_user(self, user_create: UserCreate) -> User:

        existing_user = await self.user_repo.get_user_by_email(user_create.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        hashed_password = get_password_hash(user_create.password)
        
        user_count = await User.count()
        is_first_user_admin = user_count == 0
        
        user = await self.user_repo.create_user(
            email=user_create.email,
            hashed_password=hashed_password,
            is_admin=is_first_user_admin
        )
        return user

    async def authenticate_user(self, email: EmailStr, password: str) -> Optional[User]:
        user = await self.user_repo.get_user_by_email(email)
        if not user:
            return None 
        
        if not verify_password(password, user.hashed_password):
            return None 
            
        return user

    def create_jwt_token(self, user: User) -> str:
        access_token = create_access_token(
            data={"sub": user.email}
        )
        return access_token

def get_auth_service() -> AuthService:
    return AuthService(user_repo=get_user_repository())
