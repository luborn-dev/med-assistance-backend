import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    MONGODB_URL: str = Field(..., env="MONGODB_URL")
    DATABASE_NAME: str = Field(..., env="DATABASE_NAME")


settings = Settings()


class Database:
    client: AsyncIOMotorClient = None
    database = None

    @classmethod
    async def connect(cls):
        if cls.client is None:
            cls.client = AsyncIOMotorClient(settings.MONGODB_URL)
            cls.database = cls.client[settings.DATABASE_NAME]
            print("Connected to MongoDB")

    @classmethod
    async def close_connection(cls):
        if cls.client:
            cls.client.close()
            cls.client = None
            cls.database = None
            print("Disconnected from MongoDB")

    @classmethod
    async def get_collection(cls, name: str):
        if cls.database is None:
            await cls.connect()
        return cls.database[name]


db = Database()
