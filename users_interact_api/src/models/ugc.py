from datetime import datetime
from pydantic import Field, BaseModel
from uuid import UUID

from models.model import Model


class View(Model):
    movie_id: UUID
    begin_time: datetime
    end_time: datetime


class LikesModel(Model):
    user_id: str
    film_id: str
    point: int


class FilmAvgModel(Model):
    film_id: str
    avg_vote: float


class ReviewModel(Model):
    review_id: UUID
    user_id: str
    film_id: str
    review: str
    date: datetime = Field(default_factory=datetime.now)
    likes: int | None = None


class BookmarksModel(BaseModel):
    user_id: str
    film_id: str
