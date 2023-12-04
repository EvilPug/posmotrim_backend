from fastapi import Depends, FastAPI, Request
from fastapi.applications import get_swagger_ui_html

from src.app.models import User
from src.app.db import create_db_and_tables
from src.app.users import current_active_user
from src.routers import films, auth, users, statuses

app = FastAPI(title='Posmotrim API', description='Бэкенд сервиса Посмотрим')


# Регистрация и авторизация
app.include_router(auth.auth_router, prefix="/auth/jwt", tags=['auth'])
app.include_router(auth.register_router, prefix="/auth", tags=['auth'])
app.include_router(auth.reset_password_router, prefix="/auth", tags=['auth'])
app.include_router(auth.verify_router, prefix="/auth", tags=['auth'])

# Пользователи
app.include_router(users.users_router, prefix="/users", tags=['users'])

# Фильмы
app.include_router(films.router, prefix="/films", tags=['films'])

# Статусы
app.include_router(statuses.statuses_router, prefix="/statuses", tags=['statuses'])


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)) -> dict:
    """
    Эндпоинт, который возвращается пользователю после авторизации

    :param user:  экземпляр модели User
    :return: dict
    """
    return {"message": f"Добро пожаловать {user.email}!"}


@app.on_event("startup")
async def on_startup() -> None:
    """
    Инициализация БД и таблиц в ней при запуске сервиса
    """
    await create_db_and_tables()


@app.get('/docs', include_in_schema=False)
async def get_documenatation(request: Request):
    print(request.scope)
    return get_swagger_ui_html(openapi_url=request.scope.get('root_path')+"openapi.json",
                               title='Swagger')
