from typing import List, Annotated
from uuid import UUID

from fastapi import APIRouter, status, HTTPException, Depends

from models.ugc import RequestReviewModel, ReviewResponseModel, RequestModel
from services.mongo import MongoDep, update_data, get_data, delete_data, \
    insert_data
from services.token import security_jwt, get_user_id

# Объект router, в котором регистрируем обработчики
router = APIRouter()
collection = 'reviews'


@router.post('/add-review',
             response_model=ReviewResponseModel,
             status_code=status.HTTP_201_CREATED,
             description="создание рецензии на фильм",
             response_description="user_id, movie_id, review, date, "
                                  "likes to review")
async def add_review(# token: Annotated[str, Depends(security_jwt)],
                     review: RequestReviewModel,
                     mongo: MongoDep) -> ReviewResponseModel:
    # user_id = await get_user_id(token)
    user_id = '3df47e84-a0e1-4741-81fe-fdacadd4f4f1'
    review_document = {'user_id': user_id,
                       'movie_id': review.movie_id,
                       'review': review.review}
    res = ReviewResponseModel(**review_document)
    await insert_data(mongo, res, collection)
    return res


@router.get('/list-reviews',
            response_model=List,
            status_code=status.HTTP_200_OK,
            description="получение списка рецензий к фильму",
            response_description="list of user_id, movie_id, review, date, "
                                 "likes to review")
async def list_reviews(movie: Annotated[RequestModel,
                                        Depends(RequestModel)],
                       mongo: MongoDep) -> List:
    reviews_query = {'movie_id': movie.movie_id}

    res = await get_data(mongo,
                         reviews_query,
                         collection,
                         {'movie_id': 0, '_id': 0})
    return res


@router.post('/add-like-to-review',
             response_model=ReviewResponseModel,
             status_code=status.HTTP_201_CREATED,
             description="поставить лайк на рецензию",
             response_description="user_id, movie_id, review, date, "
                                  "likes to review")
async def add_like_to_review(# token: Annotated[str, Depends(security_jwt)],
                             review: RequestReviewModel,
                             mongo: MongoDep) -> ReviewResponseModel:
    # user_id = await get_user_id(token)
    user_id = '3df47e84-a0e1-4741-81fe-fdacadd4f4f1'
    review_document = {'user_id': user_id,
                       'movie_id': review.movie_id,
                       'review': review.review}
    res = ReviewResponseModel(**review_document)
    await insert_data(mongo, res, collection)
    return res