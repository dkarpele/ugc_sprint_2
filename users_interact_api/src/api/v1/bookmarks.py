from http import HTTPStatus
from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends

from models.ugc import BookmarksRequestModel, BookmarksResponseModel
from services.mongo import MongoDep, set_data, get_data
from services.token import security_jwt, get_user_id

# Объект router, в котором регистрируем обработчики
router = APIRouter()


@router.post('/bookmarks',
             response_model=BookmarksResponseModel,
             status_code=HTTPStatus.CREATED,
             description="создание закладки на фильм",
             response_description="user_id, film_id")
async def set_document_bookmarks(token: Annotated[str, Depends(security_jwt)],
                                 bookmark: BookmarksRequestModel,
                                 mongo: MongoDep) -> BookmarksResponseModel:
    user_id = await get_user_id(token)
    # user_id = '3df47e84-a0e1-4741-81fe-fdacadd4f4f9'
    bookmark_document = {'user_id': user_id, 'movie_id': bookmark.movie_id}
    res = BookmarksResponseModel(**bookmark_document)
    await set_data(mongo, res, 'bookmarks')
    return res


@router.get('/bookmarks',
            response_model=List[UUID],
            status_code=HTTPStatus.OK,
            description="получение списка закладок пользователя",
            response_description="bookmark, begin_time, end_time")
async def get_document_bookmarks(token: Annotated[str, Depends(security_jwt)],
                                 mongo: MongoDep) -> List[UUID]:
    user_id = await get_user_id(token)
    # user_id = '3df47e84-a0e1-4741-81fe-fdacadd4f4f9'
    bookmark_query = {'user_id': user_id}

    res = await get_data(mongo, bookmark_query, 'bookmarks')
    return [elem['movie_id'] for elem in res]
