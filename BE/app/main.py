import os

from fastapi import FastAPI
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from datadog import initialize, statsd
from ddtrace import patch, config, patch_all, tracer
from app.crons.notify_expired_mecidine import setup_cron

# Datadog
# Patch is here only for those who choose not to use `ddtrace-run`
patch(fastapi=True)

tracer.configure(
    hostname='datadog',
    port=8126,
    enabled=True
)

app = FastAPI(debug=True)
oauth2_scheme = HTTPBearer(scheme_name='token')

origins = [
    "http://localhost:8088",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=["*"],
)


def setup(setup_app: FastAPI):
    from app.controllers.user.user import router as user_router
    from app.controllers.hospital.hospital import router as hospital_router
    from app.controllers.tracking_medicine.tracking_medicine import router as tracking_medicine_router
    from app.controllers.source_order_request.source_order_request import router as source_order_request_router
    from app.controllers.notification.notification import router as notification_router

    from app.infrastructure.postgresql.database import init_database

    # drop table when test in local
    init_database()

    setup_app.include_router(user_router)
    setup_app.include_router(hospital_router)
    setup_app.include_router(tracking_medicine_router)
    setup_app.include_router(source_order_request_router)
    setup_app.include_router(notification_router)

    setup_cron(app, debug=False)


setup(app)
