from logging import config as logging_config

from core.logger import LOGGING
from dotenv import load_dotenv
from pydantic import BaseSettings, Field

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)
load_dotenv()


class MainConf(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class Settings(MainConf):
    chunk_size_clickhouse: int = Field(..., env='CHUNK_SIZE_CLICKHOUSE')
    timeout_clickhouse: int = Field(..., env='TIMEOUT_CLICKHOUSE')
    clickhouse_server: str = Field(..., env='CLICKHOUSE_SERVER')
    sentry_dns: str = Field(..., env='SENTRY_DNS')

    class Config:
        env_file = '.env'


settings = Settings()


class KafkaCreds(MainConf):
    user: str = Field(..., env="KAFKA_USER")
    password: str = Field(..., env="KAFKA_PASSWORD")
    topic: str = Field(..., env='TOPIC')
    bootstrap_servers: str = Field(..., env='KAFKA_SERVERS')
    ssl_cafile: str = Field(..., env='KAFKA_CAFILE')


kafka_settings = KafkaCreds()


class LogstashCreds(MainConf):
    host: str = Field(..., env="LOGSTASH_HOST")
    port: int = Field(..., env="LOGSTASH_PORT")


logstash_settings = LogstashCreds()
