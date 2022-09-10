import json
import os
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


from app.config import get_settings

SQLALCHEMY_DATABASE_URL = get_settings().DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)
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


def seed_medicines():
    from app.infrastructure.postgresql.tracking_medicine.tracking_medicine import TrackingMedicineDTO
    from app.domains.medicine.medicine_repository import MedicineStatus
    from app.infrastructure.postgresql.source_order_request.source_order_request import SourceOrderRequestDTO

    path = os.getcwd() + '/app/resources/medicines.json'
    with open(path, 'r') as file:
        json_meds = json.load(file)

    meds_dto = list(map(lambda med: TrackingMedicineDTO(
        name=med['name'],
        status=MedicineStatus.calculate_create_status(datetime.fromisoformat(med['expired_date'])),
        expired_date=datetime.fromisoformat(med['expired_date']),
        created_at=datetime.fromisoformat(med['created_at']),
        created_by=0,
        hospital_id=0,

    ), json_meds))
    if session.query(TrackingMedicineDTO).count() == 0:
        session.add_all(meds_dto)
        session.commit()

    path = os.getcwd() + '/app/resources/source_order.json'
    with open(path, 'r') as file:
        json_meds = json.load(file)

    meds_dto = list(map(lambda med: SourceOrderRequestDTO(
        name=med['name'],
        created_by=2,

    ), json_meds))
    if session.query(SourceOrderRequestDTO).count() == 0:
        print(session.query(SourceOrderRequestDTO).count())
        session.add_all(meds_dto)
        session.commit()

    # session.add_all(meds_dto)
    # session.commit()


def init_database():
    if os.getenv('ENV', 'local') == "test":
        drop_tables()
        create_tables()
    else:
        create_tables()
        seed_medicines()

    # Seed data
