from models.user import User
from typing import Optional

class UserRepository:
    @staticmethod
    async def get_by_id(user_id: str) -> Optional[User]:
        return await User.get(user_id)

    @staticmethod
    async def create(user_data: dict) -> User:
        user = User(**user_data)
        await user.insert()
        return user

    @staticmethod
    async def update(user_id: str, update_data: dict) -> Optional[User]:
        user = await User.get(user_id)
        if not user:
            return None
        await user.update({"$set": update_data})
        return await User.get(user_id)

    @staticmethod
    async def delete(user_id: str) -> bool:
        user = await User.get(user_id)
        if not user:
            return False
        await user.delete()
        return True