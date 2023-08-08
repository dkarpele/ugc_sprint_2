import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import views
from core.config import settings
from core.logger import LOGGING

app = FastAPI(
    title="Api to analyze users behaviour",
    description="Api to analyze users behaviour",
    version="1.0.0",
    docs_url='/api/openapi-user-analyze',
    openapi_url='/api/openapi-user-analyze.json',
    default_response_class=ORJSONResponse)

app.include_router(views.router, prefix='/api/v1/views', tags=['views'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=f'{settings.host}',
        port=settings.port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
