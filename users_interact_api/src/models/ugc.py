from datetime import datetime
from uuid import UUID

from pydantic import Field

from models.model import Model


class View(Model):
    movie_id: UUID
    begin_time: datetime
    end_time: datetime


class RequestModel(Model):
    movie_id: UUID


class LikesModel(Model):
    user_id: UUID
    movie_id: UUID
    rating: int


class LikesCountMovieModel(Model):
    movie_id: UUID
    likes_count: int
    dislikes_count: int


class MovieAvgModel(Model):
    movie_id: UUID
    avg_rating: float


class RequestReviewModel(RequestModel):
    review: str


class ReviewResponseModel(Model):
    user_id: UUID
    movie_id: UUID
    review: str
    date: datetime = Field(default_factory=datetime.now)
    likes: list[dict[UUID, int]] | None = None
    likes_amount: int = 0
    dislikes_amount: int = 0


class BookmarksResponseModel(Model):
    user_id: UUID
    movie_id: UUID
