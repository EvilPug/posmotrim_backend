from fastapi import Depends
from sqlalchemy import select, Sequence, and_
from typing import AsyncGenerator, Type
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import DATABASE_URL
from src.utils.exceptions import UserNotFound, FilmNotFound
from src.app.models import Base, User, Film, Status
from src.app.schemas import StatusEnum, RatingEnum


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables() -> None:
    """
    Создает БД и таблицы
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Генератор асинхронных сессий
    """
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def db_get_user_by_id(user_id: int) -> Type[User]:
    """
    Возвращает пользователя, найденного по user_id

    :param user_id: id пользователя
    """
    async with async_session_maker() as session:
        async with session.begin():
            user = await session.get(User, user_id)
            return user


async def db_get_user_by_username(username: str) -> User:
    """
    Возвращает пользователя, найденного по username

    :param username: имя пользователя
    """

    async with async_session_maker() as session:
        async with session.begin():
            q = select(User).where(User.username == username)
            users = await session.execute(q)
            return users.scalars().first()


async def db_get_all_users() -> Sequence[User]:
    """
    Возвращает всех пользователей сервиса
    """

    async with async_session_maker() as session:
        async with session.begin():
            q = select(User)
            users = await session.execute(q)
            return users.scalars().all()


# Films
async def db_get_film(film_id: int) -> Type[Film]:
    """
     Возвращает конкретный экземпляр класса Film, полученный по film_id

     :param film_id: id фильма
     """

    async with async_session_maker() as session:
        async with session.begin():
            film = await session.get(Film, film_id)
            return film


async def db_get_top_films_by_genre(genre: str, count: int) -> Sequence[Film]:
    """
    Возвращает список размера count сущностей класса Film, в выбранном жанре.
    Фильмы отсортированы по рейтингу IMDB от лучших к худшим

    :param genre: жанр фильма
    :param count: количество фильмов, которое нужно вернуть
    """

    async with async_session_maker() as session:
        async with session.begin():
            q = select(Film).where(Film.genres.contains([genre])).order_by(Film.rating_imdb.desc()).limit(count)
            films = await session.execute(q)
            return films.scalars().all()


async def db_get_film_recommendations(film_id: int) -> Sequence[Film]:
    """
    Возвращает список рекомендованных фильмов в виде экземпляров класса Film

    :param film_id: id фильма, для которого нужны рекомендации
    """

    async with async_session_maker() as session:
        async with session.begin():

            close_q = select(Film.close_film_ids).where(Film.kinopoisk_id == film_id)
            close_ids = await session.execute(close_q)

            try:
                close_ids = close_ids.scalars().all()[0]
            except IndexError:
                close_ids = close_ids.scalars().all()

            close_films_q = select(Film).where(Film.kinopoisk_id.in_(close_ids))
            films = await session.execute(close_films_q)
            return films.scalars().all()


async def db_get_film_status(user_id: int, film_id: int) -> Status:
    """
    Возвращает статус и рейтинг, который поставил пользователь конкретному фильму

    :param user_id: id пользователя
    :param film_id: id фильма
    """

    async with async_session_maker() as session:
        async with session.begin():
            q = select(Status).where(and_(Status.user_id == user_id, Status.film_id == film_id))
            status = await session.execute(q)
            return status.scalars().first()


async def db_get_user_statuses(user_id: int) -> Sequence[Status]:
    """
    Возвращает статусы и рейтинги, который поставил пользователь фильмам

    :param user_id: id пользователя
    """

    async with async_session_maker() as session:
        async with session.begin():

            # Проверяем, что существует пользователь
            user = await db_get_user_by_id(user_id)
            if not user:
                raise UserNotFound

            q = select(Status).where(Status.user_id == user_id)
            status = await session.execute(q)
            return status.scalars().all()


async def db_create_or_update_status(user_id: int, film_id: int, status: StatusEnum, rating: RatingEnum) -> Status:
    """
    Создает и возвращает статус и рейтинг, который поставил пользователь конкретному фильму

    :param user_id: id пользователя
    :param film_id: id пользователя
    :param status: пользовательский статус фильма
    :param rating: пользовательский рейтинг фильма
    """

    async with async_session_maker() as session:
        async with session.begin():

            # Проверяем, что существует пользователь
            user = await db_get_user_by_id(user_id)
            if not user:
                raise UserNotFound

            # Проверяем, что существует фильм
            film = await db_get_film(film_id)
            if not film:
                raise FilmNotFound

            film_status = await db_get_film_status(user_id, film_id)
            if film_status:
                film_status.status = status
                film_status.rating = rating
                await session.commit()
                return film_status

            else:
                film_status = Status(
                    user_id=user_id,
                    film_id=film_id,
                    status=status,
                    rating=rating
                )
                session.add(film_status)
                await session.commit()
                return film_status

