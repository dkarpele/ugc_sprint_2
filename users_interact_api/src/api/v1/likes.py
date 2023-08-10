from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Depends

from models.ugc import RequestModel, LikesModel, MovieAvgModel
from services.mongo import MongoDep, set_data, delete_data, get_aggregated
from services.token import security_jwt, get_user_id

# Объект router, в котором регистрируем обработчики
router = APIRouter()
collection = 'likes'


@router.post('/like',
             response_model=LikesModel,
             status_code=status.HTTP_201_CREATED,
             description="создание like на фильм",
             response_description="user_id, film_id, point")
async def set_like(token: Annotated[str, Depends(security_jwt)],
                   like: RequestModel,
                   mongo: MongoDep) -> LikesModel:
    user_id = await get_user_id(token)
    # user_id = '6df47e84-a0e1-4741-81fe-fdacadd4f4f9'
    like_document = {'user_id': user_id,
                     'movie_id': like.movie_id,
                     'point': 10}
    res = LikesModel(**like_document)
    await set_data(mongo,
                   {'user_id': user_id,
                    'movie_id': like.movie_id},
                   res,
                   collection)
    return res


@router.post('/dislike',
             response_model=LikesModel,
             status_code=status.HTTP_201_CREATED,
             description="создание dislike на фильм",
             response_description="user_id, film_id, point")
async def set_dislike(token: Annotated[str, Depends(security_jwt)],
                      dislike: RequestModel,
                      mongo: MongoDep) -> LikesModel:
    user_id = await get_user_id(token)
    # user_id = '3df47e84-a0e1-4741-81fe-fdacadd4f4f9'
    like_document = {'user_id': user_id,
                     'movie_id': dislike.movie_id,
                     'point': 0}
    res = LikesModel(**like_document)
    await set_data(mongo,
                   {'user_id': user_id,
                    'movie_id': dislike.movie_id},
                   res,
                   collection)
    return res


@router.get('/avg-movie-rating',
            response_model=MovieAvgModel,
            status_code=status.HTTP_200_OK,
            description="получение средней оценки за фильм",
            response_description="movie_id, rating")
async def average_movie_rating(movie: Annotated[RequestModel,
                                                Depends(RequestModel)],
                               mongo: MongoDep) -> MovieAvgModel:
    avg_query = [
        {
            '$match': {
                'movie_id': movie.movie_id
            }
        },
        {
            '$group': {
                '_id': "$movie_id",
                'avg_rating': {
                    '$avg': "$point"
                }
            }
        }
    ]
    res = await get_aggregated(mongo, avg_query, collection)
    if len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Movie not found!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    first_res = res[0]
    first_res['movie_id'] = first_res.pop('_id')
    first_res['avg_rating'] = round(first_res['avg_rating'], 1)
    return MovieAvgModel(**first_res)


@router.delete('/like',
               status_code=status.HTTP_204_NO_CONTENT,
               description="удаление like or dislike у юзера", )
async def delete_like(token: Annotated[str, Depends(security_jwt)],
                      like: RequestModel,
                      mongo: MongoDep):
    user_id = await get_user_id(token)
    # user_id = '3df47e84-a0e1-4741-81fe-fdacadd4f4f9'
    like_document = {'user_id': user_id, 'movie_id': like.movie_id}
    res = await delete_data(mongo,
                            like_document,
                            collection)
    if res.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Like not found!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        return True