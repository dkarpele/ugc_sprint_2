from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient

from db.mongo import get_mongo, Mongo
from core.config import mongo_settings
from models.model import Model


@lru_cache()
def get_mongo_service(
        mongo: Mongo = Depends(get_mongo)) -> Mongo:
    return mongo


MongoDep = Annotated[Mongo, Depends(get_mongo_service)]


async def set_data(
        db: AsyncIOMotorClient,
        document: Model,
        collection: str,
) -> None:
    """Save doc in Mongo db
    Args:
        :param db: MongoDB
        :param document: Document to upload
        :param collection: Collection name
    """
    db_name = mongo_settings.db
    db = db.client[db_name]
    await db[collection].insert_one(jsonable_encoder(document))


async def get_data(
        db: AsyncIOMotorClient,
        query: dict | str,
        collection: str,
) -> list:
    """Get doc from Mongo db
    Args:
        :param db: MongoDB
        :param query: Request to find
        :param collection: Collection name
    """
    db_name = mongo_settings.db
    db = db.client[db_name]
    res = db[collection].find(query)
    documents_list = []
    async for document in res:
        documents_list.append(document)

    return documents_list
