from typing import Dict, List, Optional
from sqlalchemy import exc
import logging
from sqlalchemy.sql import select
from app.infrastructure.postgresql.hospital.hospital import HospitalDTO
from app.domains.helpers.database_repository import DatabaseRepository


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
