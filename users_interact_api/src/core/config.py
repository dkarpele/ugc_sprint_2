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
    host: str = Field(..., env='HOST_USERS_ANALYZE')
    port: int = Field(..., env='PORT_USERS_ANALYZE')
    host_auth: str = Field(..., env='HOST_AUTH')
    port_auth: int = Field(..., env='PORT_AUTH')


settings = Settings()


class KafkaCreds(MainConf):
    user: str = Field(..., env="KAFKA_USER")
    password: str = Field(..., env="KAFKA_PASSWORD")
    topic: str = Field(..., env='TOPIC')
    bootstrap_servers: list = Field(..., env='KAFKA_SERVERS').split()
    ssl_cafile: str = Field(..., env='KAFKA_CAFILE')


kafka_settings = KafkaCreds()