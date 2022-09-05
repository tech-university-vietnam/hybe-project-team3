from fastapi import FastAPI
from fastapi.security import HTTPBearer
import os
app = FastAPI(debug=True)

reusable_oauth2 = HTTPBearer(scheme_name='Authorization', auto_error=False)


def setup(setup_app: FastAPI):
    from app.controllers.user.user import router as user_router
    from app.controllers.hospital.hospital import router as hospital_router
    from app.infrastructure.postgresql.database import (
        create_tables,
        drop_tables)
    # drop table when test in local
    if os.getenv('ENV', 'local') in ["test"]:
        drop_tables()
    create_tables()

    setup_app.include_router(user_router)
    setup_app.include_router(hospital_router)


setup(app)
