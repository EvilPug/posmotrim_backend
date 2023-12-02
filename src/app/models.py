from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import String, func, BigInteger, DateTime, Integer, Float


class Base(DeclarativeBase):
    """
    Это база.
    """
    pass


class User(SQLAlchemyBaseUserTable, Base):
    """
    Модель пользователя, построенная на SQLAlchemy ORM
    """

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    birthday: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "User(id=%s, username='%s', created_at='%s')" % (
            self.id,
            self.username,
            self.created_at
        )


class Film(Base):
    """
    Модель фильма, построенная на SQLAlchemy ORM
    """

    __tablename__ = 'films'

    kinopoisk_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    slogan: Mapped[str] = mapped_column(String(1024), nullable=True)
    description: Mapped[str] = mapped_column(String(4096), nullable=True)
    genres: Mapped[list] = mapped_column(ARRAY(String(32)), nullable=True)
    rating_imdb: Mapped[float] = mapped_column(Float, nullable=True)
    year: Mapped[int] = mapped_column(Integer)
    film_length: Mapped[int] = mapped_column(Integer, nullable=True)
    close_film_ids: Mapped[list] = mapped_column(ARRAY(Integer), nullable=True)

    def __repr__(self):
        return "Film(kinopoisk_id=%s, name='%s', year='%s')" % (
            self.kinopoisk_id,
            self.name,
            self.year
        )
