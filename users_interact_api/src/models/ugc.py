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
    point: int


class MovieAvgModel(Model):
    movie_id: UUID
    avg_rating: float


class ReviewModel(Model):
    review_id: UUID
    user_id: UUID
    movie_id: UUID
    review: str
    date: datetime = Field(default_factory=datetime.now)
    likes: int | None = None


class BookmarksResponseModel(Model):
    user_id: UUID
    movie_id: UUID
