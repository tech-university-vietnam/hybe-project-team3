from fastapi import FastAPI
from functools import lru_cache
from fastapi.security import HTTPBearer
from app.config import Settings
from app.infrastructure.postgresql.database import create_tables


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
app = FastAPI(debug=True)

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)


def setup(setup_app: FastAPI):
    from app.controllers.auth.auth import router as auth_router
    from app.controllers.user.user import router as user_router
    from app.controllers.hospital.hospital import router as hospital_router

    create_tables()

    setup_app.include_router(auth_router)
    setup_app.include_router(user_router)
    setup_app.include_router(hospital_router)


setup(app)
