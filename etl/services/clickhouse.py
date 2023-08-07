import logging
import time
from clickhouse_driver import Client
from clickhouse_driver.errors import Error
from kafka import KafkaConsumer

from models.views import ClickHouseModel
from services.backoff import backoff


class ClickHouseLoader:
    def __init__(self, consumer: KafkaConsumer, clickhouse: Client) -> None:
        self.consumer = consumer
        self.clickhouse = clickhouse
        self.start_time = time.time()
        self.cache = []

    @backoff(service='Kafka')
    def get_data(self, chunk_size: int = 1000) -> None:
        for msg in self.consumer:
            user_id, film_id = msg.key.decode("utf-8").split("%")
            begin_time, end_time = msg.value.decode("utf-8").split("%")

            self.cache.append(ClickHouseModel(
                user_id=user_id,
                film_id=film_id,
                begin_time=begin_time,
                end_time=end_time
            ))

            if time.time() > self.start_time + 5:
                logging.info(f'{len(self.cache)} messages arrived to broker:\n'
                             f'{self.cache}')
                self.write_to_clickhouse(self.cache)
                self.cache = []
                self.start_time = time.time()
            if len(self.cache) >= chunk_size:
                logging.info(f'{len(self.cache)} messages arrived to broker:\n'
                             f'{self.cache}')
                self.write_to_clickhouse(self.cache)
                self.cache = []
                self.start_time = time.time()

    @backoff(service='ClickHouse')
    def write_to_clickhouse(self, cache):
        insert_record = """
        INSERT INTO user_viewed_frame (user_id, film_id, begin_time, end_time) 
        VALUES {data};
        """
        query = insert_record.format(
            data=", ".join([f"('{i.user_id}', "
                            f"'{i.film_id}', "
                            f"parseDateTimeBestEffort('{i.begin_time}'), "
                            f"parseDateTimeBestEffort('{i.end_time}'))"
                            for i in cache])
        )

        try:
            self.clickhouse.execute(query)
            logging.info(f"Inserting to clickhouse...\n{query}")
        except Error as err:
            logging.error(err)
