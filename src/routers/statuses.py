from typing import Optional
from fastapi import APIRouter, Depends, status, HTTPException, Form

from src.app.users import current_user
from src.app.schemas import StatusEnum, RatingEnum, StatusUpdate
from src.utils.exceptions import UserNotFound, FilmNotFound
from src.app import db

statuses_router = APIRouter()


@statuses_router.get(
    path="/{user_id}/{film_id}",
    dependencies=[Depends(current_user)],
    name="statuses:get_film_status",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The Film status does not exist",
        },
    },
)
async def get_film_status(user_id: int, film_id: int):
    """
    Возвращает статус и рейтинг, который поставил пользователь конкретному фильму

    :param user_id: id пользователя
    :param film_id: id фильма
    """
    film_status = await db.db_get_film_status(user_id, film_id)
    if film_status:
        return film_status
    else:
        raise HTTPException(status_code=404,
                            detail="The film status does not exist")


@statuses_router.get(
    path="/{user_id}",
    dependencies=[Depends(current_user)],
    name="statuses:get_user_statuses",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User does not exist or has no statuses",
        },
    },
)
async def get_user_statuses(user_id: int):
    """
    Возвращает все статусы фильмов пользователя

    :param user_id: id пользователя
    """

    try:
        user_statuses = await db.db_get_user_statuses(user_id)

        if user_statuses:
            return user_statuses
        else:
            raise HTTPException(status_code=404,
                                detail="User has no statuses")

    except UserNotFound:
        raise HTTPException(status_code=404,
                            detail="User does not exist")


@statuses_router.get(
    path="/get_user_statuses_by_status/{user_id}/{film_status}",
    dependencies=[Depends(current_user)],
    name="statuses:get_user_statuses_by_status",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User does not exist or has no statuses",
        },
    },
)
async def get_user_statuses_by_status(user_id: int, film_status: StatusEnum):
    """
    Возвращает статусы и рейтинги, который поставил пользователь фильмам с фильтром по статусу

    :param user_id: id пользователя
    :param film_status: статус
    """

    try:
        user_statuses = await db.db_get_user_statuses_by_status(user_id, film_status)

        if user_statuses:
            return user_statuses
        else:
            raise HTTPException(status_code=404,
                                detail="User has no statuses")

    except UserNotFound:
        raise HTTPException(status_code=404,
                            detail="User does not exist")


@statuses_router.post(
    path="/update/{user_id}/{film_id}/{status}/{rating}",
    response_model=StatusUpdate,
    dependencies=[Depends(current_user)],
    name="statuses:get_user_statuses",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User or Film does not exist",
        },
    },
)
async def create_or_update_status(film_status: StatusUpdate):
    """
    Создает/редактирует объект Status в базе данных и возвращает его

    :param user_id: id пользователя
    :param film_id: id фильма
    :param status: статус фильма пользователя
    :param rating: пользовательский рейтинг фильма от 1 до 10
    """

    print(current_user)

    try:
        film_status = await db.db_create_or_update_status(film_status.user_id,
                                                          film_status.film_id,
                                                          film_status.status,
                                                          film_status.rating)
        return film_status
    except UserNotFound:
        raise HTTPException(status_code=404,
                            detail="User does not exist")
    except FilmNotFound:
        raise HTTPException(status_code=404,
                            detail="Film does not exist")
