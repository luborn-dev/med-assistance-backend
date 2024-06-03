from unittest.mock import patch

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from app.config.database import Database, Settings


@pytest.fixture
def mongo_settings():
    # Configuração fictícia para testes
    return Settings(MONGODB_URL="mongodb://localhost:27017", DATABASE_NAME="test_db")


@pytest.fixture
async def database(mongo_settings):
    # Usando patch para substituir o cliente MongoDB por um cliente mongomock
    with patch.object(
        Database, "client", new=AsyncIOMotorClient(mongo_settings.MONGODB_URL)
    ):
        await Database.connect()
        yield Database
        await Database.close_connection()


@pytest.mark.asyncio
async def test_database_connection(database):
    assert database.client is not None
    assert database.database is not None
    assert database.client.address[0] == "localhost"


@pytest.mark.asyncio
async def test_get_collection(database):
    collection_name = "test_collection"
    collection = await database.get_collection(collection_name)
    assert collection.name == collection_name
