from sqlalchemy import exc, delete, update, desc
import logging

from sqlalchemy.orm import joinedload

from app.common.exceptions import DBError
from app.domains.source_order_request.source_order_request_exceptions import RequestNotExistError
from app.infrastructure.postgresql.source_order_request.source_order_request import SourceOrderRequestDTO
from app.domains.helpers.database_repository import DatabaseRepository
from app.model.source_order_request import SourceOrderRequest, SourceOrderHospitalRequest, SourceOrderRequestPayload


class SourceOrderRequestRepository:
    def __init__(self, database_repository: DatabaseRepository):
        self.db_repo = database_repository
        self.db = next(self.db_repo.get_db())

    def create(self, data: SourceOrderRequestPayload):
        try:
            source_order_request_dto = SourceOrderRequestDTO.from_data(data)
            self.db.add(source_order_request_dto)
            self.db.commit()
            return source_order_request_dto.to_entity()
        except exc.SQLAlchemyError as e:
            logging.error(e)
            raise DBError

    def list(self, hospital_id: int):
        try:
            source_orders: [SourceOrderRequestDTO] = self.db.query(SourceOrderRequestDTO). \
                filter(SourceOrderRequestDTO.hospital_id == hospital_id). \
                order_by(desc(SourceOrderRequestDTO.created_at)).all()
            return [order.to_entity() for order in source_orders]
        except exc.SQLAlchemyError as e:
            logging.error(e)
            raise DBError

    def update(self, data, source_id, user_id):
        try:
            source_order_req_dto = self.db.query(SourceOrderRequestDTO).filter(
                (SourceOrderRequestDTO.id == source_id)).first()
            updated_values = {**dict(data)}
            if source_order_req_dto is None:
                raise RequestNotExistError
            stmt = (
                update(SourceOrderRequestDTO).
                where(SourceOrderRequestDTO.id == source_id).
                values(updated_values)
            )
            self.db.execute(stmt)
            self.db.commit()
        except exc.SQLAlchemyError as e:
            logging.error(e)
            raise DBError

    def get(self, id: int) -> SourceOrderHospitalRequest:
        source_order_dto: SourceOrderRequestDTO = self.db.query(SourceOrderRequestDTO).options(
            joinedload(SourceOrderRequestDTO.hospital)).get(id)

        return source_order_dto.to_full_entity()

    def delete(self, id: int) -> bool:
        statement = delete(SourceOrderRequestDTO).where(SourceOrderRequestDTO.id == id)
        try:
            self.db.execute(statement)
            self.db.commit()
            return True
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return False
