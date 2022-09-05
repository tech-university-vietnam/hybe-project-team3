import logging
from typing import Optional

from sqlalchemy import exc, delete, update

from app.controllers.tracking_medicine.tracking_medicine import TrackingMedicinePayload
from app.domains.helpers.database_repository import DatabaseRepository
from app.infrastructure.postgresql.tracking_medicine.tracking_medicine import TrackingMedicineDTO
from app.model.tracking_medicine import TrackingMedicine


class MedicalRepository:
    """User Repository defines a repository interface for user entity."""

    def __init__(self, database_repository: DatabaseRepository):
        self.db_repo = database_repository
        self.db = self.db_repo.db

    def list(self):
        return self.db.query(TrackingMedicineDTO).all()

    def get(self, id: int) -> Optional[TrackingMedicine]:
        medicine_dto: TrackingMedicineDTO = self.db.query(TrackingMedicineDTO).filter(
            (TrackingMedicineDTO.id == id)).first()

        return medicine_dto and medicine_dto.to_entity()

    def create(self, medicine: TrackingMedicinePayload) -> Optional[TrackingMedicine]:
        try:
            medicine_dto = TrackingMedicineDTO.from_tracking_medicine_payload(medicine)
            self.db.add(medicine_dto)
            self.db.commit()
            logging.info(medicine_dto)
            return medicine_dto.to_entity()
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return

    def update(self, id: int, medicine: TrackingMedicinePayload) -> Optional[TrackingMedicine]:
        try:
            medicine_dto: Optional[TrackingMedicineDTO] = self.db.query(TrackingMedicineDTO).filter(
                (TrackingMedicineDTO.id == id)).first()
            if medicine_dto is None:
                return
            update_values = {**dict(medicine_dto.to_entity()), **dict(medicine)}
            stmt = (
                update(TrackingMedicineDTO).
                where(TrackingMedicineDTO.id == id).
                values(update_values)
            )

            self.db.execute(stmt)
            self.db.commit()

            return medicine_dto.to_entity()
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return

    def delete_by_id(self, id: str) -> bool:
        statement = delete(TrackingMedicineDTO).where(TrackingMedicineDTO.id == id)
        try:
            self.db.execute(statement)
            self.db.commit()
            return True
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return False
