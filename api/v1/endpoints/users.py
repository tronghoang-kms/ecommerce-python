from fastapi import APIRouter, Depends
from schemas.user import UserRead
from models.user import User
from security.auth import get_current_user

router = APIRouter()

@router.get("/me", response_model=UserRead)
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    return current_user
