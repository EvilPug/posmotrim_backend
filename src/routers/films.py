from fastapi import APIRouter

from src.app.db import db_get_film, db_get_film_recommendations, db_get_top_films_by_genre

router = APIRouter()


@router.get("/{film_id}")
async def get_film(film_id: int):
    """
    Возвращает конкретный экземпляр класса Film, полученный по film_id

    :param film_id: id фильма
    """
    film = await db_get_film(film_id)
    return film


@router.get("/top_films_by_genre/{genre}/{count}")
async def get_top_films_by_genre(genre: str, count: int):
    """
    Возвращает список размера count сущностей класса Film, в выбранном жанре.
    Фильмы отсортированы по рейтингу IMDB от лучших к худшим

    :param genre: жанр фильма
    :param count: количество фильмов, которое нужно вернуть
    """
    films = await db_get_top_films_by_genre(genre, count)
    return films


@router.get("/{film_id}/recommendations")
async def get_film_recommendations(film_id: int):
    """
    Возвращает список рекомендованных фильмов в виде экземпляров класса Film

    :param film_id: id фильма, для которого нужны рекомендации
    """
    film = await db_get_film_recommendations(film_id)
    return film
