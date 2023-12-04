from fastapi import APIRouter, HTTPException, status

from src.utils.exceptions import FilmNotFound
from src.app.db import db_get_film, db_get_film_recommendations, db_get_top_films_by_genre

router = APIRouter()


@router.get(
    path="/{film_id}",
    name="films:get_film",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The Film does not exist",
        },
    },
)
async def get_film(film_id: int):
    """
    Возвращает конкретный экземпляр класса Film, полученный по film_id

    :param film_id: id фильма
    """
    try:
        film = await db_get_film(film_id)
        return film
    except FilmNotFound:
        raise HTTPException(status_code=404, detail="Film does not exist")


@router.get(
    path="/top_films_by_genre/{genre}/{count}",
    name="films:get_top_films_by_genre",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The genre does not exist",
        },
    },
)
async def get_top_films_by_genre(genre: str, count: int):
    """
    Возвращает список размера count сущностей класса Film, в выбранном жанре.
    Фильмы отсортированы по рейтингу IMDB от лучших к худшим

    :param genre: жанр фильма
    :param count: количество фильмов, которое нужно вернуть
    """
    films = await db_get_top_films_by_genre(genre, count)
    if films:
        return films
    else:
        raise HTTPException(status_code=404,
                            detail="The genre does not exist")


@router.get(
    path="/{film_id}/recommendations",
    name="films:get_film_recommendations",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The Film does not exist",
        },
    },
)
async def get_film_recommendations(film_id: int):
    """
    Возвращает список рекомендованных фильмов в виде экземпляров класса Film

    :param film_id: id фильма, для которого нужны рекомендации
    """
    try:
        films = await db_get_film_recommendations(film_id)
        return films
    except FilmNotFound:
        raise HTTPException(status_code=404, detail="Film does not exist")
