from src.app.users import fastapi_users
from src.app.schemas import UserRead, UserUpdate


users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
