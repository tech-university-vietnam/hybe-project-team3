import json
import os
import datetime
from datetime import datetime
import random
import bcrypt


def seed_medicines(session):
    from app.infrastructure.postgresql.tracking_medicine.tracking_medicine import TrackingMedicineDTO
    from app.domains.medicine.medicine_repository import MedicineStatus
    from app.infrastructure.postgresql.user.user_dto import UserDTO
    if session.query(TrackingMedicineDTO).count() == 0:
        path = os.getcwd() + '/app/resources/medicines.json'
        with open(path, 'r') as file:
            json_meds = json.load(file)

        users = session.query(UserDTO).all()
        max_user = session.query(UserDTO).count()
        meds_dto = []
        for med in json_meds:
            user = users[random.randint(0, max_user - 1)]
            meds_dto.append(
                TrackingMedicineDTO(
                    name=med['name'],
                    status=MedicineStatus.calculate_create_status(datetime.fromisoformat(med['expired_date'])),
                    expired_date=datetime.fromisoformat(med['expired_date']),
                    created_at=datetime.fromisoformat(med['created_at']),
                    created_by=user.id,
                    hospital_id=user.work_for,
                ))
        session.add_all(meds_dto)
        session.commit()


def seed_sources(session):
    from app.infrastructure.postgresql.source_order_request.source_order_request import SourceOrderRequestDTO
    if session.query(SourceOrderRequestDTO).count() == 0:
        path = os.getcwd() + '/app/resources/source_order.json'
        with open(path, 'r') as file:
            json_sources = json.load(file)

        sources_dto = list(map(lambda source: SourceOrderRequestDTO(
            name=source['name'],
            created_by=source['created_by'],

        ), json_sources))

        session.add_all(sources_dto)
        session.commit()


def hash_pw(user):
    salt = bcrypt.gensalt()
    password = user['password'].encode('utf8')
    pwhash = bcrypt.hashpw(password, salt).decode('utf8')
    return pwhash


def seed_users(session):
    from app.infrastructure.postgresql.user.user_dto import UserDTO
    if session.query(UserDTO).count() == 0:
        path = os.getcwd() + '/app/resources/users.json'
        with open(path, 'r') as file:
            json_file = json.load(file)

        user_dtos = list(map(lambda user: UserDTO(
            email=user['email'],
            hash_pw=hash_pw(user),
            work_for=user['work_for']
        ), json_file))
        session.add_all(user_dtos)
        session.commit()


def seed_hositals(session):
    from app.infrastructure.postgresql.hospital.hospital import HospitalDTO
    if session.query(HospitalDTO).count() == 0:
        path = os.getcwd() + '/app/resources/hospitals.json'
        with open(path, 'r') as file:
            json_sources = json.load(file)

        hospital_dtos = list(map(lambda source: HospitalDTO(
            name=source['name'],
            telephone=source['telephone'],
            address=source['address'],

        ), json_sources))
        session.add_all(hospital_dtos)
        session.commit()


def seed_notifications(session):
    from app.infrastructure.postgresql.notiffication.notification import NotificationDTO
    if session.query(NotificationDTO).count() == 0:
        path = os.getcwd() + '/app/resources/notifications.json'
        with open(path, 'r') as file:
            json_sources = json.load(file)

        hospital_dtos = list(map(lambda source: NotificationDTO(
            ['name'],
            telephone=source['telephone'],
            address=source['address'],

        ), json_sources))
        session.add_all(hospital_dtos)
        session.commit()
