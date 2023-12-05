from typing import Optional
from datetime import datetime
from enum import Enum, IntEnum
from pydantic import BaseModel, Field


from fastapi_users import schemas


class StatusEnum(Enum):
    watching = 'Смотрю'
    watched = 'Посмотрел'
    plan = 'Буду смотреть'
    quit = 'Бросил'


class RatingEnum(IntEnum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10


class UserRead(schemas.BaseUser):
    """
    Схема пользователя
    """

    username: str
    birthday: datetime
    created_at: datetime


class UserCreate(schemas.BaseUserCreate):
    """
    Схема пользователя с дефолтными значениями при создании
    """

    username: str
    birthday: datetime
    created_at: datetime = Field(default_factory=datetime.now, hidden=True)


class UserUpdate(schemas.BaseUserUpdate):
    """
    Схема с полями пользователя, которые доступны для изменения
    """

    username: Optional[str] = None
    birthday: Optional[datetime] = None


class FilmRead(BaseModel):
    """
    Схема фильма
    """

    kinopoisk_id: int
    name: int
    slogan: str
    description: str
    genres: list
    rating_imdb: float
    year: int
    film_length: int
    close_film_ids: list


class StatusRead(BaseModel):
    """
    Схема статуса
    """
    id: int
    status: StatusEnum
    rating: RatingEnum
    user_id: int
    film_id: int


class StatusUpdate(BaseModel):
    """
    Схема статуса с необходимыми полями при создании или изменении
    """
    user_id: int
    film_id: int
    status: Optional[StatusEnum] = None
    rating: Optional[RatingEnum] = None
