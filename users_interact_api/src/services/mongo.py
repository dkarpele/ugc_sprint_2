from functools import lru_cache
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import errors
from pymongo.results import DeleteResult

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
        query: Model | dict,
        update: Model | dict,
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
        await db[collection].update_one(jsonable_encoder(query),
                                        {"$set": jsonable_encoder(update)},
                                        upsert=True)
    except errors.PyMongoError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err,
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_data(
        db: AsyncIOMotorClient,
        query: dict | str,
        collection: str,
        projection: str | None = None
) -> list:
    """Get doc from Mongo db
    Args:
        :param projection: which fields are returned in the matching documents.
        :param db: MongoDB
        :param query: Request to find
        :param collection: Collection name
    """
    db_name = mongo_settings.db
    db = db.client[db_name]
    if projection:
        res = db[collection].find(jsonable_encoder(query),
                                  {projection: 1})
    else:
        res = db[collection].find(jsonable_encoder(query),)
    documents_list = []
    async for document in res:
        documents_list.append(document)

    if not projection:
        return documents_list
    else:
        return [elem[projection] for elem in documents_list]


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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err,
            headers={"WWW-Authenticate": "Bearer"},
        )
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
    count = await db[collection].count_documents(jsonable_encoder(query),)

    return count
