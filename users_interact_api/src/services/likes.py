from bson import ObjectId
from fastapi import HTTPException, status

from models.ugc import RequestReviewIdModel, LikedReviewModel, RequestModel, \
    LikesModel
from services.mongo import MongoDep, update_data, get_count
from services.token import get_user_id


async def add_like_to_review_helper(review: RequestReviewIdModel,
                                    mongo: MongoDep,
                                    token: str | None = None,
                                    rating: int = 10) -> LikedReviewModel:
    # check if review_id really exists
    review_exists = await get_count(
        mongo,
        {'_id': ObjectId(review.review_id)},
        'reviews')
    if review_exists == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'{review.review_id} review does not exist',
                            headers={"WWW-Authenticate": "Bearer"},)

    collection = 'review_likes'
    user_id = await get_user_id(token)

    # add info about review_id, user_id, his like/dislike to review_likes
    query = {'user_id': user_id,
             'review_id': ObjectId(review.review_id)}
    review_document = {'user_id': user_id,
                       'review_id': ObjectId(review.review_id),
                       'rating': rating}
    await update_data(mongo, query, review_document, collection)

    # get likes_amount/dislikes_amount from review_likes

    liked_review_amount = await get_count(
        mongo,
        {'review_id': ObjectId(review.review_id),
         'rating': 10},
        collection)
    disliked_review_amount = await get_count(
        mongo,
        {'review_id': ObjectId(review.review_id),
         'rating': 0},
        collection)

    # add data about likes_amount/dislikes_amount to reviews by review_id(_id)
    likes_amount_doc = {'likes_amount': liked_review_amount,
                        'dislikes_amount': disliked_review_amount}
    await update_data(mongo,
                      {'_id': ObjectId(review.review_id)},
                      likes_amount_doc,
                      'reviews')

    review_document['review_id'] = str(review_document.get('review_id'))
    res = LikedReviewModel(**review_document)
    return res


async def set_like_to_movie_helper(like: RequestModel,
                                   mongo: MongoDep,
                                   token: str | None = None,
                                   rating: int = 10) -> LikesModel:
    collection = 'likes'
    user_id = await get_user_id(token)

    like_document = {'user_id': user_id,
                     'movie_id': str(like.movie_id),
                     'rating': rating}
    res = LikesModel(**like_document)
    await update_data(mongo,
                      {'user_id': user_id,
                       'movie_id': str(like.movie_id)},
                      like_document,
                      collection)
    return res
