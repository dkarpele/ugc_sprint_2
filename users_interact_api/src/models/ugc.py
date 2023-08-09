from datetime import datetime
from uuid import UUID

from pydantic import Field

from models.model import Model


class View(Model):
    movie_id: UUID
    begin_time: datetime
    end_time: datetime


class LikesModel(Model):
    user_id: UUID
    film_id: UUID
    point: int


class FilmAvgModel(Model):
    film_id: UUID
    avg_vote: float


class ReviewModel(Model):
    review_id: UUID
    user_id: UUID
    film_id: UUID
    review: str
    date: datetime = Field(default_factory=datetime.now)
    likes: int | None = None


class BookmarksRequestModel(Model):
    movie_id: UUID


class BookmarksResponseModel(Model):
    user_id: UUID
    movie_id: UUID
