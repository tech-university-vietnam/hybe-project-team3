from fastapi import FastAPI
from functools import lru_cache
from app.config import Settings
from app.infrastructure.postgresql.database import create_tables


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
app = FastAPI(debug=True)


def setup(setup_app: FastAPI):
    from app.controllers.auth.auth import router as auth_router
    from app.controllers.user import router as user_router

    create_tables()

    setup_app.include_router(auth_router)
    setup_app.include_router(user_router)


setup(app)
