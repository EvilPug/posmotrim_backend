from typing import Optional
from datetime import datetime, UTC
from fastapi_users import schemas


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


class FilmRead:
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
