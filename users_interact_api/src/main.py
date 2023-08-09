import logging
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import views, bookmarks
from core.config import settings, mongo_settings
from core.logger import LOGGING
from db import mongo


async def startup():
    mongo.mongo = mongo.Mongo(
        f'mongodb://{mongo_settings.user}:{mongo_settings.password}'
        f'@{mongo_settings.host}:{mongo_settings.port}'
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

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=f'{settings.host}',
        port=settings.port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
