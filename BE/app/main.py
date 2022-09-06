from fastapi import FastAPI
from app.infrastructure.postgresql import init_db
import os

if os.getenv('ENV', 'local') == "test":
    print('go here')
    init_db(test=True)
else:
    init_db(test=False)
app = FastAPI(debug=True)


def setup(setup_app: FastAPI):
    from app.controllers.user.user import router as user_router
    from app.controllers.hospital.hospital import router as hospital_router
    from app.infrastructure.postgresql.database import (
        create_tables,
        drop_tables)
    # drop table when test in local
    if os.getenv('ENV', 'local') == "test":
        drop_tables()
    create_tables()

    setup_app.include_router(user_router)
    setup_app.include_router(hospital_router)


setup(app)
