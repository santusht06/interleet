from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGO_URI, DB_NAME

import os
from dotenv import load_dotenv

load_dotenv()


# MONGO_URI = os.getenv("MONGO_URI")
# DB_NAME = os.getenv("DB_NAME")

print(MONGO_URI)

if not MONGO_URI or not DB_NAME:
    raise RuntimeError("MONGO_URI or DB_NAME not set in environment")


client = AsyncIOMotorClient(MONGO_URI)

database = client[DB_NAME]


async def get_db():
    try:
        yield database

    finally:
        pass
