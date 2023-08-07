import uuid

from datetime import datetime

from models.model import Model


class ClickHouseModel(Model):
    user_id: uuid.UUID
    film_id: uuid.UUID
    begin_time: datetime
    end_time: datetime
