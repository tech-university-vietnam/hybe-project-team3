from fastapi import FastAPI
from fastapi.security import HTTPBearer
import os
app = FastAPI(debug=True)

reusable_oauth2 = HTTPBearer(scheme_name='Authorization')


def setup(setup_app: FastAPI):
    from app.controllers.user.user import router as user_router
    from app.controllers.hospital.hospital import router as hospital_router
    from app.controllers.tracking_medicine.tracking_medicine import router as tracking_medicine_router

    from app.infrastructure.postgresql.database import init_database

    # drop table when test in local
    init_database()

    setup_app.include_router(user_router)
    setup_app.include_router(hospital_router)
    setup_app.include_router(tracking_medicine_router)


setup(app)
