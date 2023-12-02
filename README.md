# FastAPI бэкенд сервиса "Посмотрим"

## Технологии
- FastAPI
- PostgreSQL
- SQLAlchemy
- pydantic

## Запуск проекта
1) Разверните БД PostgreSQL (локально или докер-контейнер)

2) Склонируйте проект
   ```
   git clone https://github.com/EvilPug/posmotrim_backend.git
   ```

3) Добавьте переменную окружения
   ```
   export PYTHONPATH="${PYTHONPATH}:~/posmotrim_backend/"
   ```

4) Создайте в корне проекта .env файл (рядом с requirements.txt) и замените значения на свои:
    ```
    # Переменные, связанные с БД
    DB_HOST='postgres'
    DB_PORT=5432
    DB_USER='postgres'
    DB_PASS='postgres'
    DB_NAME='postgres'
    
    # Секретный ключ. Можно сгенерировать с помощью команды: openssl rand -hex 32
    SECRET='super_secret_key'
    ```

5) Создайте и активируйте виртуальное окружение:
    ```
   python3 -m venv venv
   . ./venv/bin/activate
    ```

6) Установите зависимости
    ```
   pip3 install -r requirements.txt
    ```

7) Запустите сервис:
    ```
   python3 ./src/main.py
    ```

8) Наполните таблицу films фильмами:
    ```
   python3 ./src/data/populate_films.py
    ```

9) Сервис доступен по адресу:
    ```
   http://localhost:8000
    ```

10) Если вам нужен другой адрес вы можете изменить его в main файле или запустить сервис командой (изменив значения):
   ```
   uvicorn src.app.app:app --host 127.0.0.1 --port 8000 --reload 
   ```
