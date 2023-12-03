from src.app.schemas import UserCreate, UserRead
from src.app.users import auth_backend, fastapi_users


auth_router = fastapi_users.get_auth_router(auth_backend)
auth_router.prefix = "/auth/jwt"
auth_router.tags = ["auth"]

register_router = fastapi_users.get_register_router(UserRead, UserCreate)
register_router.prefix = "/auth"
register_router.tags = ["auth"]

reset_password_router = fastapi_users.get_reset_password_router()
reset_password_router.prefix = "/auth"
reset_password_router.tags = ["auth"]

verify_router = fastapi_users.get_verify_router(UserRead)
verify_router.prefix = "/auth"
verify_router.tags = ["auth"]
