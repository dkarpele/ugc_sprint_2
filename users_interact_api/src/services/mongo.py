from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import errors
from pymongo.results import DeleteResult

from db.mongo import get_mongo, Mongo
from core.config import mongo_settings
from models.model import Model
from services.exceptions import entity_doesnt_exist


@lru_cache()
def get_mongo_service(
        mongo: Mongo = Depends(get_mongo)) -> Mongo:
    return mongo


MongoDep = Annotated[Mongo, Depends(get_mongo_service)]


async def insert_data(
        db: AsyncIOMotorClient,
        insert: Model | dict,
        collection: str,
) -> None:
    """Save doc in Mongo db
    Args:
        :param db: MongoDB
        :param insert: Document to insert
        :param collection: Collection name
    """
    db_name = mongo_settings.db
    db = db.client[db_name]
    try:
        await db[collection].insert_one(jsonable_encoder(insert))
    except errors.PyMongoError as err:
        raise entity_doesnt_exist(err)


async def update_data(
        db: AsyncIOMotorClient,
        query: dict,
        update: dict,
        collection: str,
) -> None:
    """Save doc in Mongo db
    Args:
        :param db: MongoDB
        :param update: Document to upload
        :param query: document to match
        :param collection: Collection name
    """
    db_name = mongo_settings.db
    db = db.client[db_name]
    try:
        await db[collection].update_one(query,
                                        {"$set": update},
                                        upsert=True)
    except errors.PyMongoError as err:
        raise entity_doesnt_exist(err)


async def get_data(
        db: AsyncIOMotorClient,
        query: dict | str,
        collection: str,
        projection: dict | None = None,
        sort: tuple | None = None
) -> list:
    """Get doc from Mongo db
    Args:
        :param sort: tuple = ('sort_by', 1 or -1 for asc or desc)
        :param projection: which fields are returned in the matching documents.
        :param db: MongoDB
        :param query: Request to find
        :param collection: Collection name
    """
    if not sort:
        sort = ('_id', 1)
    db_name = mongo_settings.db
    db = db.client[db_name]

    res = db[collection].find(jsonable_encoder(query),
                              projection).sort(*sort)

    documents_list = []
    async for document in res:
        documents_list.append(document)

    return documents_list


async def delete_data(
        db: AsyncIOMotorClient,
        document: Model | dict,
        collection: str,
) -> DeleteResult:
    """Delete doc from collection in Mongo db
    Args:
        :param db: MongoDB
        :param document: Document to delete
        :param collection: Collection name
    """
    db_name = mongo_settings.db
    db = db.client[db_name]
    try:
        res = await db[collection].delete_one(jsonable_encoder(document),)
    except errors.PyMongoError as err:
        raise entity_doesnt_exist(err)
    return res


async def get_aggregated(
        db: AsyncIOMotorClient,
        query: dict | str | list,
        collection: str,
) -> list:
    """Get aggregated doc from Mongo db
    Args:
        :param db: MongoDB
        :param query: Request to find
        :param collection: Collection name
    """
    db_name = mongo_settings.db
    db = db.client[db_name]
    cursor = db[collection].aggregate(jsonable_encoder(query),)
    docs = await cursor.to_list(None)

    return docs


async def get_count(
        db: AsyncIOMotorClient,
        query: dict | str | list,
        collection: str,
) -> list:
    """Get doc's count from Mongo db
    Args:
        :param db: MongoDB
        :param query: Request to find
        :param collection: Collection name
    """
    db_name = mongo_settings.db
    db = db.client[db_name]
    count = await db[collection].count_documents(query)

    return count
