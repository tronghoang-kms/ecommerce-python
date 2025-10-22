from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def test_connection():
    client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    dbs = await client.list_database_names()
    print(dbs)


if __name__ == "__main__":
    asyncio.run(test_connection())
