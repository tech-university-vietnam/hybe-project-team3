from sqlalchemy import exc, delete, update, desc, or_, and_
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

    def list(self, hospital_id):
        """
        warningExpired -> show only for from_hospital
        notifyAvailable -> show only for to_hospital
        notifySold -> show for both hospital
        """
        try:
            result = list(map(lambda m: m.to_entity(),
            self.db.query(NotificationDTO).filter(
                or_(
                    and_(NotificationDTO.type == "warningExpired",
                         NotificationDTO.from_hospital_id == hospital_id),
                    and_(NotificationDTO.type == "notifyAvailable",
                         NotificationDTO.to_hospital_id == hospital_id),
                    and_(NotificationDTO.type == "notifySold",
                         or_(
                            NotificationDTO.to_hospital_id == hospital_id,
                            NotificationDTO.from_hospital_id == hospital_id,
                         )
                    )
                )
                ).order_by(
                desc(NotificationDTO.created_at)).all()))
            # change seen status
            mappings = []
            for item in result:
                mappings.append({
                    "id": item.id,
                    "seen_status": "Seen"
                })
            self.db.bulk_update_mappings(NotificationDTO, mappings)
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

    def get_notseen_number(self, hospital_id):
        count :int= self.db.query(NotificationDTO).filter(or_(NotificationDTO.from_hospital_id == hospital_id, NotificationDTO.to_hospital_id == hospital_id), NotificationDTO.seen_status=="Not seen").count()
        return count

    def update_status(self, id: int, status: str):
        """
        Update notification status
        if status is Approved -> change type to notifySold
        """
        try:
            update_values = {
                "status": status,
            }
            if status == "Approved":
                if self.db.query(NotificationDTO).filter(
                    NotificationDTO.id == id,
                    NotificationDTO.type == "notifyAvailable"):
                    update_values["type"] = "notifySold"
            # stmt = (
            #     update(NotificationDTO).
            #     where(NotificationDTO.id == id).
            #     values(update_values)
            # )
            stmt = NotificationDTO.update().returning(NotificationDTO) \
                .where(NotificationDTO.id == id) \
                .values(update_values)
            self.db.execute(stmt)
            noti = self.db.commit()
            return noti
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return
