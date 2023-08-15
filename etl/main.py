import logging
from clickhouse_driver import Client
from clickhouse_driver.errors import Error
from kafka import KafkaConsumer

from core.config import settings, kafka_settings
from services.clickhouse import ClickHouseLoader
import sentry_sdk

sentry_sdk.init(
    dsn=settings.sentry_dns,
    traces_sample_rate=1.0
)


def etl_clickhouse() -> None:
    """ETL from Kafka to ClickHouse"""
    clickhouse_loader = ClickHouseLoader(
        consumer=KafkaConsumer(
            kafka_settings.topic,
            bootstrap_servers=kafka_settings.bootstrap_servers.split(),
            # auto_offset_reset='earliest',
            # enable_auto_commit=False,
            security_protocol="SASL_SSL",
            sasl_mechanism="SCRAM-SHA-512",
            sasl_plain_username=kafka_settings.user,
            sasl_plain_password=kafka_settings.password,
            ssl_cafile=kafka_settings.ssl_cafile,
            consumer_timeout_ms=settings.timeout_clickhouse * 1000
        ),
        clickhouse=Client(settings.clickhouse_server)
    )
    while True:
        clickhouse_loader.get_data(chunk_size=5)


if __name__ == '__main__':
    client = Client(host=settings.clickhouse_server)
    try:
        client.execute(
            """
        CREATE TABLE IF NOT EXISTS user_viewed_frame
        (
            user_id UUID,
            film_id UUID,
            begin_time DateTime,
            end_time DateTime
        ) engine=MergeTree()
        ORDER BY (user_id, film_id);
        """
        )
    except Error as err:
        logging.error(err)

    etl_clickhouse()
