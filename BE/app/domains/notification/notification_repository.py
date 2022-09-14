import logging
from typing import List, Iterator, Union

from sqlalchemy import update, exc, and_, or_, desc
from sqlalchemy.orm import joinedload

from app.domains.helpers.database_repository import DatabaseRepository
from app.infrastructure.postgresql.notiffication.notification import NotificationDTO
from app.model.notification import Notification, Status, SeenStatus, NotificationWithHospital, Type


class NotificationRepository(DatabaseRepository):

    def list(self, hospital_id: int) -> List[NotificationWithHospital]:
        notifies: [NotificationDTO] = self.db.query(NotificationDTO).options(
            joinedload(NotificationDTO.from_hospital),
            joinedload(NotificationDTO.to_hospital)
        ).filter(
            or_(
                and_(NotificationDTO.type == Type.warning_expired,
                     NotificationDTO.from_hospital_id == hospital_id),
                and_(NotificationDTO.type == Type.notify_available,
                     NotificationDTO.to_hospital_id == hospital_id),
                and_(NotificationDTO.type == Type.notify_sold,
                         NotificationDTO.from_hospital_id == hospital_id,
                     ))
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
                and_(NotificationDTO.type == Type.warning_expired,
                     NotificationDTO.from_hospital_id == hospital_id),
                and_(NotificationDTO.type == Type.notify_available,
                     NotificationDTO.to_hospital_id == hospital_id),
                and_(NotificationDTO.type == Type.notify_sold,
                     NotificationDTO.from_hospital_id == hospital_id)
            ),
            NotificationDTO.seen_status == SeenStatus.not_seen
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
            notify: NotificationDTO = self.db.query(NotificationDTO).get(id)
            if not notify or status not in Status.all():
                return

            notify.status = status
            if status == Status.approved and notify.type == Type.notify_available:
                print("run")
                self.db.add(
                    NotificationDTO.from_approved_request(notify)
                )
                self.db.commit()

            self.db.flush([notify])
            self.db.commit()
            return notify
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return

    def update_status_to_invalid(self, id: int):
        try:
            invalid_notis = self.db.query(NotificationDTO).filter(
                NotificationDTO.sourcing_id == id,
                NotificationDTO.type == Type.notify_available,
                NotificationDTO.status == Status.init
            ).all()
            mappings = []
            for noti in invalid_notis:
                mappings.append({
                    "id": noti.id,
                    "status": Status.invalid
                })
            self.db.bulk_update_mappings(NotificationDTO, mappings)
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return
