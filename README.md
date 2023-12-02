# FastAPI бэкенд сервиса "Посмотрим"

## Технологии
- FastAPI
- PostgreSQL
- SQLAlchemy
- pydantic

## Запуск проекта
1) Создайте в корне проекта .env файл (рядом с requirements.txt) и заполните его:
    ```
    # Переменные, связанные с БД
    DB_HOST=''
    DB_PORT=''
    DB_USER=''
    DB_PASS=''
    DB_NAME=''
    
    # Секретный ключ. Можно сгенерировать с помощью команды: openssl rand -hex 32
    SECRET=''
    ```

2) Создайте и активируйте виртуальное окружение:
    ```
   python3 -m venv venv
   . ./venv/bin/activate
    ```

3) Запустите сервис:
    ```
   python3 ./src/main.py
    ```

4) Наполните таблицу films фильмами:
    ```
   python3 ./src/data/populate_films.py
    ```
5) PROFIT!!!
