from enum import Enum
from datetime import datetime, UTC
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict, EmailStr


from fastapi_users import schemas


class StatusEnum(Enum):
    watching = 'Смотрю'
    watched = 'Посмотрел'
    plan = 'Буду смотреть'
    quit = 'Бросил'


Rating = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


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
    created_at: datetime = datetime.now(UTC)


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
    rating: Rating
    user_id: int
    film_id: int


class StatusCreate(BaseModel):
    status: StatusEnum
    rating: Rating
    user_id: int
    film_id: int


class StatusUpdate(BaseModel):
    status: StatusEnum
    rating: Rating
