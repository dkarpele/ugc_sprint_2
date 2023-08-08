from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from db.kafka_db import get_kafka, Kafka
from db.mongo import get_mongo, Mongo
from kafka import KafkaProducer


@lru_cache()
def get_kafka_producer(
        kafka: Kafka = Depends(get_kafka)):
    return kafka


@lru_cache()
def get_mongo_service(
        mongo: Mongo = Depends(get_mongo)) -> Mongo:
    return mongo


KafkaDep = Annotated[KafkaProducer, Depends(get_kafka_producer)]
MongoDep = Annotated[Mongo, Depends(get_mongo_service)]
