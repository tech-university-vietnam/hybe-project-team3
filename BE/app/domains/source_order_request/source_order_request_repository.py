from sqlalchemy import exc, delete, update
import logging
from app.common.exceptions import DBError
from app.domains.source_order_request.source_order_request_exceptions import RequestNotExistError
from app.infrastructure.postgresql.source_order_request.source_order_request import SourceOrderRequestDTO
from app.domains.helpers.database_repository import DatabaseRepository


class SourceOrderRequestRepository:
    def __init__(self, database_repository: DatabaseRepository):
        self.db_repo = database_repository
        self.db = next(self.db_repo.get_db())

    def create(self, data):
        try:
            source_order_request_dto = SourceOrderRequestDTO.from_data(data)
            self.db.add(source_order_request_dto)
            self.db.commit()
            return source_order_request_dto.to_entity()
        except exc.SQLAlchemyError as e:
            logging.error(e)
            raise DBError

    def list(self):
        try:
            result = list(map(lambda m: m.to_entity(), self.db.query(SourceOrderRequestDTO).all()))
            return result
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
                where(SourceOrderRequestDTO.id == source_id, SourceOrderRequestDTO.created_by == user_id).
                values(updated_values)
            )
            self.db.execute(stmt)
            self.db.commit()
        except exc.SQLAlchemyError as e:
            logging.error(e)
            raise DBError
    # def check_user_id(self):
    #     item = self.db.query(SourceOrderRequestDTO).filter(SourceOrderRequestDTO.id == id, SourceOrderRequestDTO.created_by == id)
    #     return bool(item.id)

    # TODO: check the hospital id if user id is not matched
    def delete(self, id, user_id):
        statement = delete(SourceOrderRequestDTO).where(SourceOrderRequestDTO.id == id, SourceOrderRequestDTO.created_by == user_id)
        try:
            self.db.execute(statement)
            self.db.commit()
        except exc.SQLAlchemyError as e:
            logging.error(e)
            raise DBError