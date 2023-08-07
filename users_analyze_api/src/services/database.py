from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from db.kafka_db import get_kafka, Kafka
from kafka import KafkaProducer


@lru_cache()
def get_kafka_producer(
        db: Kafka = Depends(get_kafka)):
    return db


KafkaDep = Annotated[KafkaProducer, Depends(get_kafka_producer)]
