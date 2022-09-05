from typing import Dict, List, Optional
from sqlalchemy import exc
import logging
from sqlalchemy.sql import select
from app.infrastructure.postgresql.hospital.hospital_dto import HospitalDTO
from app.domains.helpers.database_repository import DatabaseRepository

HOSPITAL_NAMES = [
    "Hồ Chí Minh city 115 Emergency center"
    "Hồ Chí Minh city International Medical quarantine center",
    "Hồ Chí Minh city Preventive health center",
    "Hồ Chí Minh city Center for Health Protection of labor and environmental",
    "Hồ Chí Minh city Center for Reproductive Health Care",
    "Hồ Chí Minh city Center of Forensic",
    "1st district hospital and Preventive health center",
    "2nd district hospital and Preventive health center",
    "3rd district hospital and Preventive health center",
    "4th district hospital and Preventive health center",
    "5th district hospital and Preventive health center",
    "6th district hospital and Preventive health center",
    "7th district hospital and Preventive health center",
    "8th district hospital and Preventive health center",
    "9th district hospital and Preventive health center",
    "10th district hospital and Preventive health center"
]


class HospitalRepository:
    def __init__(self, database_repository: DatabaseRepository):
        self.db_repo = database_repository
        self.db = next(self.db_repo.get_db())

    def get_hospitals(self) -> Optional[List[Dict]]:
        statement = select(HospitalDTO.id, HospitalDTO.name)
        try:
            results: List = self.db.execute(statement)
            hospital_list = []
            for row in results:
                hospital_list.append({"id": row[0], "name": row[1]})
            return hospital_list
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return None

    def seed_hospitals(self) -> Optional[List]:
        try:
            results = self.db.query(HospitalDTO).all()
            if not results:
                results = [
                    HospitalDTO.from_mock_data(
                        name=name, telephone='Fake phone number',
                        address="fake address") for name in HOSPITAL_NAMES]
                self.db.bulk_save_objects(results, return_defaults=True)
                self.db.commit()
                return results
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return None
