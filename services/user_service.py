from repositories.user_repository import UserRepository
from schemas.user import UserCreate, UserUpdate
from models.user import User

class UserService:
    @staticmethod
    async def create_user(user_data: UserCreate) -> User:
        # Check username uniqueness
        existing_user = await User.find_one(User.username == user_data.username)
        if existing_user:
            raise ValueError("Username already exists")
        return await UserRepository.create(user_data.dict())

    @staticmethod
    async def get_user(user_id: str) -> User:
        user = await UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user

    @staticmethod
    async def update_user(user_id: str, user_data: UserUpdate) -> User:
        user = await UserRepository.update(user_id, user_data.dict(exclude_unset=True))
        if not user:
            raise ValueError("User not found")
        return user

    @staticmethod
    async def delete_user(user_id: str) -> bool:
        success = await UserRepository.delete(user_id)
        if not success:
            raise ValueError("User not found")
        return success
