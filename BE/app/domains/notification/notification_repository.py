import logging
from typing import List, Iterator, Union

from sqlalchemy import update, exc, func, and_, or_, desc
from sqlalchemy.orm import joinedload

from app.domains.helpers.database_repository import DatabaseRepository
from app.infrastructure.postgresql.notiffication.notification import NotificationDTO
from app.model.notification import Notification, Status, SeenStatus, NotificationWithHospital


class NotificationRepository(DatabaseRepository):

    def list(self, hospital_id: int) -> List[NotificationWithHospital]:
        notifies: [NotificationDTO] = self.db.query(NotificationDTO).filter(
            or_(
                and_(NotificationDTO.type == "warningExpired",
                     NotificationDTO.from_hospital_id == hospital_id),
                and_(NotificationDTO.type == "notifyAvailable",
                     NotificationDTO.to_hospital_id == hospital_id),
                and_(NotificationDTO.type == "notifySold",
                     or_(
                         NotificationDTO.to_hospital_id == hospital_id,
                         NotificationDTO.from_hospital_id == hospital_id,
                     )))
        ).order_by(
            desc(NotificationDTO.created_at)).all()
        return list(map(lambda notify: notify.to_full_entity(), notifies))

    def approved(self, id: int):
        return self._update_status(id, 'approved')

    def declined(self, id: int):
        return self._update_status(id, 'declined')

    def _update_status(self, id: int, new_status: str) -> bool:
        if new_status not in Status.all():
            return False

        try:
            stmt = (
                update(NotificationDTO).
                values(status=new_status).
                where(NotificationDTO.id == id)
            )
            self.db.execute(stmt)
            self.db.commit()
            return True
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return False

    def count_total_not_seen(self, hospital_id: int) -> int:
        count = self.db.query(NotificationDTO).filter(
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
            ),
            NotificationDTO.seen_status == "Not seen"
        ).count()
        return count

    def update_all_seen_status(self, ids: Iterator[int]):
        if not ids:
            return
        try:
            stmt = (
                update(NotificationDTO).
                values(seen_status=SeenStatus.seen).
                where(NotificationDTO.id.in_(ids))
            )
            self.db.execute(stmt)
            self.db.commit()
            return True
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return False

    def create(self, payload: Union[List[Notification], Notification]):
        if isinstance(payload, Notification):
            payload = [payload]

        dto_payloads = list(map(lambda p: NotificationDTO.from_notification_payload(p), payload))
        self.db.add_all(dto_payloads)
        self.db.commit()

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
