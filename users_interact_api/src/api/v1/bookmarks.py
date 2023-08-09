from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from models.ugc import View, BookmarksModel
from services.database import KafkaDep, MongoDep
from services.token import security_jwt, get_user_id

# Объект router, в котором регистрируем обработчики
router = APIRouter()


@router.post('/bookmarks',
             status_code=HTTPStatus.CREATED,
             description="создание записи о просмотре",
             response_description="movie_id, begin_time, end_time")
async def set_document_bookmarks(token: Annotated[str, Depends(security_jwt)],
                                 bookmark: BookmarksModel,
                                 mongo: MongoDep) -> None:
    user_id = await get_user_id(token)
    await kafka.produce_viewed_frame(user_id,
                                     view.movie_id,
                                     view.begin_time,
                                     view.end_time)
    view_dto = jsonable_encoder(view)
    view_dto['user_id'] = user_id
    return view_dto
