import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.config import get_settings
from app.infrastructure.postgresql import seeders

SQLALCHEMY_DATABASE_URL = get_settings().DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
session: Session = SessionLocal()

Base = declarative_base()


def import_models():
    from app.infrastructure.postgresql.user.user_dto import UserDTO
    from app.infrastructure.postgresql.tracking_medicine.tracking_medicine import TrackingMedicineDTO
    from app.infrastructure.postgresql.hospital.hospital import HospitalDTO
    from app.infrastructure.postgresql.source_order_request.source_order_request import SourceOrderRequestDTO
    from app.infrastructure.postgresql.notiffication.notification import NotificationDTO

    return [UserDTO, TrackingMedicineDTO, HospitalDTO, SourceOrderRequestDTO, NotificationDTO]


def create_tables():
    Base.metadata.create_all(bind=engine)


def drop_tables():
    Base.metadata.drop_all(bind=engine)


def init_database():

    if os.getenv('ENV', 'local') == "test":
        drop_tables()
        create_tables()
        seeders.seed_hositals(session)
    else:
        create_tables()
        seeders.seed_hositals(session)
        seeders.seed_users(session)
        seeders.seed_medicines(session)
        seeders.seed_sources(session)
