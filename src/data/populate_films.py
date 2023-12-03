import pandas as pd
from asyncio import run
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import String, Integer, ARRAY

from src.app.db import async_session_maker
from src.utils.logging import logging
from src.config import DATABASE_URL


engine = create_async_engine(DATABASE_URL)


async def main():
    """
    Скрипт-функция. Загружает фильмы из csv файлов, добавляет рекомендации и загружает данные в БД
    """

    df = pd.read_csv('films_data.csv',
                     converters={'genres': pd.eval},
                     dtype_backend='numpy_nullable')

    column_labels = {'kinopoiskId': 'kinopoisk_id',
                     'ratingImdb': 'rating_imdb',
                     'filmLength': 'film_length'}

    df.rename(columns=column_labels, inplace=True)

    columns = ['kinopoisk_id', 'name', 'slogan', 'description', 'genres',
               'rating_imdb', 'year', 'film_length']

    df = df[columns]

    df_close = pd.read_csv('close_films.csv',
                           converters={'close_film_ids': pd.eval},
                           dtype_backend='numpy_nullable')

    df['close_film_ids'] = df_close['close_film_ids']

    dtypes = {'genres': ARRAY(String(32)), 'close_film_ids': ARRAY(Integer)}

    # Записываем датафрейм в БД
    async with async_session_maker() as session:
        conn = await session.connection()
        await conn.run_sync(
            lambda sync_conn: df.to_sql(
                'films',
                con=sync_conn,
                if_exists='replace',
                index=False,
                dtype=dtypes
            ),
        )
        await session.commit()


if __name__ == '__main__':
    run(main())
    logging.info('Таблица films успешно заполнена!')
