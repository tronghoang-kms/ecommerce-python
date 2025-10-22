from fastapi import APIRouter, HTTPException
from schemas.user import UserCreate, UserRead, UserUpdate
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate):
    try:
        db_user = await UserService.create_user(user)
        return db_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: str):
    try:
        user = await UserService.get_user(user_id)
        return user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{user_id}", response_model=UserRead)
async def update_user(user_id: str, user_data: UserUpdate):
    try:
        user = await UserService.update_user(user_id, user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    try:
        await UserService.delete_user(user_id)
        return {"detail": "User deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))