from sqlalchemy import exc, delete, update, desc
import logging
from app.common.exceptions import DBError
from app.infrastructure.postgresql.notiffication.notification import NotificationDTO
from app.domains.helpers.database_repository import DatabaseRepository


class NotificationRepository:
    def __init__(self, database_repository: DatabaseRepository):
        self.db_repo = database_repository
        self.db = next(self.db_repo.get_db())

    def create(self, data):
        try:
            notification_dto = NotificationDTO.from_data(data)
            self.db.add(notification_dto)
            self.db.commit()
            return notification_dto.to_entity()
        except exc.SQLAlchemyError as e:
            logging.error(e)
            raise DBError

    def list(self):
        try:
            result = list(map(lambda m: m.to_entity(),
            self.db.query(NotificationDTO).order_by(
                desc(NotificationDTO.created_at)).all()))
            return result
        except exc.SQLAlchemyError as e:
            logging.error(e)
            raise DBError

    def update(self, data, source_id, user_id):
        try:
            stmt = self.db.query(NotificationDTO).filter(
                (NotificationDTO.id == source_id)).first()
            updated_values = {**dict(data)}
            stmt = (
                update(NotificationDTO).
                where(NotificationDTO.id == source_id, NotificationDTO.created_by == user_id).
                values(updated_values)
            )
            self.db.execute(stmt)
            self.db.commit()
        except exc.SQLAlchemyError as e:
            logging.error(e)
            raise DBError

    # TODO: check the hospital id if user id is not matched
    def delete(self, id, user_id):
        statement = delete(NotificationDTO).where(NotificationDTO.id == id, NotificationDTO.created_by == user_id)
        try:
            self.db.execute(statement)
            self.db.commit()
        except exc.SQLAlchemyError as e:
            logging.error(e)
            raise DBError