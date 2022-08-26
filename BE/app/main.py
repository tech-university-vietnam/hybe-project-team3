from fastapi import FastAPI
from fastapi.security import HTTPBearer

app = FastAPI(debug=True)

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)


def setup(setup_app: FastAPI):
        <<<<<<< HEAD
    from app.controllers.hospital.hospital import router as hospital_router
    from app.infrastructure.postgresql.database import create_tables
    # drop_tables()
    create_tables()

    setup_app.include_router(auth_router)
    setup_app.include_router(user_router)
    setup_app.include_router(hospital_router)


setup(app)
