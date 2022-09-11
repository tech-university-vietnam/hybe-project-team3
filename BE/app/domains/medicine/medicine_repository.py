import logging
from datetime import datetime
from typing import Optional, List

from sqlalchemy import exc, delete, update, desc

from app.controllers.tracking_medicine.tracking_medicine import TrackingMedicinePayload
from app.domains.helpers.database_repository import DatabaseRepository
from app.infrastructure.postgresql.tracking_medicine.tracking_medicine import TrackingMedicineDTO
from app.model.tracking_medicine import TrackingMedicine
from app.model.user import DetailUser


class MedicineStatus:

    @staticmethod
    def calculate_create_status(expired_date: datetime):
        _now = datetime.utcnow()

        if _now <= expired_date.replace(tzinfo=None):
            return 'Not listed'
        else:
            return 'Expired'

    # def


class MedicineRepository(MedicineStatus):
    """User Repository defines a repository interface for user entity."""

    def __init__(self, database_repository: DatabaseRepository):
        self.db_repo = database_repository
        self.db = self.db_repo.db

    def list(self) -> List[TrackingMedicine]:
        return list(map(lambda m: m.to_entity(),
                    self.db.query(TrackingMedicineDTO).order_by(
                    desc(TrackingMedicineDTO.created_at)).all()))

    def get(self, id: int) -> Optional[TrackingMedicine]:
        medicine_dto: TrackingMedicineDTO = self.db.query(TrackingMedicineDTO).filter(
            (TrackingMedicineDTO.id == id)).first()

        return medicine_dto and medicine_dto.to_entity()

    def get_by_name(self, name: str) -> Optional[List[TrackingMedicine]]:
        medicine_list: [TrackingMedicineDTO] = self.db.query(TrackingMedicineDTO).filter(
            (TrackingMedicineDTO.name == name)).all()
        return medicine_list

    # def get_listed_medicine_quantity_by_name(self, name: str) -> Optional[List[TrackingMedicine]]:
    #     listed_medicine_quantity: TrackingMedicineDTO = self.db.query(TrackingMedicineDTO).filter(
    #         (TrackingMedicineDTO.name == name)).count()
    #     return listed_medicine_quantity

    # def get_listed_medicine_by_name(self, name: str) -> Optional[List[TrackingMedicine]]:
    #     listed_medicine_quantity: TrackingMedicineDTO = self.db.query(TrackingMedicineDTO).filter(
    #         (TrackingMedicineDTO.name == name,)).count()
    #     return listed_medicine_quantity

    def create(self, medicine: TrackingMedicinePayload, user: DetailUser) -> Optional[TrackingMedicine]:
        try:
            medicine_dto = TrackingMedicineDTO.from_tracking_medicine_payload(medicine)
            medicine_dto.status = MedicineStatus.calculate_create_status(medicine_dto.expired_date)
            medicine_dto.hospital_id = user.work_for
            medicine_dto.created_by = user.id

            self.db.add(medicine_dto)
            self.db.commit()
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

    def delete(self, id: int) -> bool:
        statement = delete(TrackingMedicineDTO).where(TrackingMedicineDTO.id == id)
        try:
            self.db.execute(statement)
            self.db.commit()
            return True
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return False
