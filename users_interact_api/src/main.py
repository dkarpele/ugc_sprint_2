import logging
import sentry_sdk
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import views, bookmarks, likes
from core.config import settings, mongo_settings
from core.logger import LOGGING
from db import mongo



sentry_sdk.init(
    dsn="https://d324786bda153d6c542e33449a3dd06b@o4505697103380480.ingest.sentry.io/4505697180516352",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)


async def startup():
    if mongo_settings.user and mongo_settings.password:
        mongo.mongo = mongo.Mongo(
            f'mongodb://'
            f'{mongo_settings.user}:{mongo_settings.password}@'
            f'{mongo_settings.host}:{mongo_settings.port}'
        )
    else:
        mongo.mongo = mongo.Mongo(
            f'mongodb://'
            f'{mongo_settings.host}:{mongo_settings.port}'
        )


async def shutdown():
    pass


@asynccontextmanager  # type: ignore[arg-type]
async def lifespan(app: FastAPI):
    await startup()
    yield

app = FastAPI(
    title="Api to analyze users behaviour",
    description="Api to analyze users behaviour",
    version="1.0.0",
    docs_url='/api/openapi-user-analyze',
    openapi_url='/api/openapi-user-analyze.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,)

app.include_router(views.router, prefix='/api/v1/views', tags=['views'])
app.include_router(bookmarks.router, prefix='/api/v1/bookmarks',
                   tags=['bookmarks'])
app.include_router(likes.router, prefix='/api/v1/likes',
                   tags=['likes'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=f'{settings.host}',
        port=settings.port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
