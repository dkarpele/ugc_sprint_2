from typing import List, Annotated
from uuid import UUID

from fastapi import APIRouter, status, HTTPException, Depends

from models.ugc import RequestModel, BookmarksResponseModel
from services.mongo import MongoDep, set_data, get_data, delete_data
from services.token import security_jwt, get_user_id

# Объект router, в котором регистрируем обработчики
router = APIRouter()
collection = 'bookmarks'


@router.post('/bookmarks',
             response_model=BookmarksResponseModel,
             status_code=status.HTTP_201_CREATED,
             description="создание закладки на фильм",
             response_description="user_id, film_id")
async def set_document_bookmarks(token: Annotated[str, Depends(security_jwt)],
                                 bookmark: RequestModel,
                                 mongo: MongoDep) -> BookmarksResponseModel:
    user_id = await get_user_id(token)
    # user_id = '3df47e84-a0e1-4741-81fe-fdacadd4f4f9'
    bookmark_document = {'user_id': user_id, 'movie_id': bookmark.movie_id}
    res = BookmarksResponseModel(**bookmark_document)
    await set_data(mongo, res, res, collection)
    return res


@router.get('/bookmarks',
            response_model=List[UUID],
            status_code=status.HTTP_200_OK,
            description="получение списка закладок пользователя",
            response_description="movie_id")
async def get_document_bookmarks(token: Annotated[str, Depends(security_jwt)],
                                 mongo: MongoDep) -> List[UUID]:
    user_id = await get_user_id(token)
    # user_id = '3df47e84-a0e1-4741-81fe-fdacadd4f4f9'
    bookmark_query = {'user_id': user_id}

    res = await get_data(mongo, bookmark_query, collection, 'movie_id')
    return res


@router.delete('/bookmarks',
               status_code=status.HTTP_204_NO_CONTENT,
               description="удаление закладки у юзера",)
async def delete_document_bookmarks(
                            token: Annotated[str, Depends(security_jwt)],
                            bookmark: RequestModel,
                            mongo: MongoDep):
    user_id = await get_user_id(token)
    # user_id = '3df47e84-a0e1-4741-81fe-fdacadd4f4f9'
    bookmark_document = {'user_id': user_id, 'movie_id': bookmark.movie_id}
    res = await delete_data(mongo,
                            BookmarksResponseModel(**bookmark_document),
                            collection)
    if res.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bookmark not found!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        return True
