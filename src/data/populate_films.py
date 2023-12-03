import pandas as pd
from asyncio import run
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import String, Integer, ARRAY

from src.app.db import async_session_maker
from src.utils.logging import logging
from src.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL)


async def df_to_db(df: pd.DataFrame, table_name: str, dtypes: dict) -> None:
    """
    Загружает датафрейм в БД

    :param df: датафрейм
    :param table_name: название таблицы
    :param dtypes: типы данных, которые нужно задать явно
    """

    async with async_session_maker() as session:
        conn = await session.connection()
        await conn.run_sync(
            lambda sync_conn: df.to_sql(
                name=table_name,
                con=sync_conn,
                if_exists='replace',
                index=False,
                dtype=dtypes
            ),
        )
        await session.commit()


def get_films_df(csv_path: str) -> pd.DataFrame:
    """
    Возвращает датафрейм с фильмами, загруженный из csv-файла

    :param csv_path: путь до csv-файла
    """

    films_df = pd.read_csv(filepath_or_buffer=csv_path,
                           converters={'genres': pd.eval},
                           dtype_backend='numpy_nullable')

    column_labels = {'kinopoiskId': 'kinopoisk_id',
                     'ratingImdb': 'rating_imdb',
                     'filmLength': 'film_length'}

    films_df.rename(columns=column_labels, inplace=True)

    columns = ['kinopoisk_id', 'name', 'slogan', 'description', 'genres',
               'rating_imdb', 'year', 'film_length']

    films_df = films_df[columns]
    return films_df


def get_close_films_df(csv_path: str) -> pd.DataFrame:
    """
    Возвращает датафрейм с похожими фильмами, загруженный из csv-файла

    :param csv_path: путь до csv-файла
    """

    df_close = pd.read_csv(filepath_or_buffer=csv_path,
                           converters={'close_film_ids': pd.eval},
                           dtype_backend='numpy_nullable')

    return df_close


async def main():

    films_df = get_films_df('films_data.csv')
    close_df = get_close_films_df('close_films.csv')

    films_df['close_film_ids'] = close_df['close_film_ids']

    dtypes = {'genres': ARRAY(String(32)), 'close_film_ids': ARRAY(Integer)}

    # Записываем датафрейм в БД
    await df_to_db(df=films_df, table_name='films', dtypes=dtypes)

    logging.info('Таблица films успешно заполнена!')


if __name__ == '__main__':
    run(main())
