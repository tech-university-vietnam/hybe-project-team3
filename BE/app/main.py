from fastapi import FastAPI
from fastapi.security import HTTPBearer
from app.infrastructure.postgresql import init_db

init_db(show_logs=True)

app = FastAPI(debug=True)

reusable_oauth2 = HTTPBearer(scheme_name='Authorization', auto_error=False)


def setup(setup_app: FastAPI):
    from app.controllers.user.user import router as user_router
    from app.controllers.hospital.hospital import router as hospital_router

    setup_app.include_router(user_router)
    setup_app.include_router(hospital_router)


setup(app)
