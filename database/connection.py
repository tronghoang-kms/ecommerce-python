from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from core.config import settings
from models.user import User
from models.product import Product
from models.cart import Cart
from models.order import Order

async def init_db():
    print(f"Connecting to MongoDB at {settings.MONGODB_URL}...")
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    
    db_name = settings.MONGO_DB_NAME
    
    await init_beanie(
        database=client[db_name],
        document_models=[
            User,
            Product,
            Cart,
            Order
        ]
    )
    print(f"Beanie initialized with database '{db_name}'")
