from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
from dotenv import load_dotenv

from models.user import User

load_dotenv()

async def init_db():
    client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    db_name = os.getenv("MONGO_DB_NAME")
    await init_beanie(database=client[db_name], document_models=[User])
