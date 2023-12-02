from fastapi import Depends, FastAPI

from src.app.models import User
from src.app.db import create_db_and_tables
from src.app.schemas import UserCreate, UserRead, UserUpdate
from src.app.users import auth_backend, current_active_user, fastapi_users

from src.routers import films

app = FastAPI(title='Posmotrim API', description='Бэкенд сервиса Посмотрим')

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(
    films.router
)


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
    Инициализация БД и таблиц в ней
    """
    await create_db_and_tables()
