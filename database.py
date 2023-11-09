from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

from settings import settings

# синхронный доступ к БД
client = MongoClient(settings.DATABASE_URL)
db = client[settings.DB_NAME]
collection = db[settings.DB_COLLECTION]

# асинхронный доступ к БД
async_client = AsyncIOMotorClient(settings.DATABASE_URL)
async_db = async_client[settings.DB_NAME]
async_collection = async_db[settings.DB_COLLECTION]
