import logging
from typing import List, Iterator

from sqlalchemy import update, exc, func, and_

from app.domains.helpers.database_repository import DatabaseRepository
from app.infrastructure.postgresql.notiffication.notification import NotificationDTO
from app.model.notification import Notification, Status, SeenStatus


class NotificationRepository(DatabaseRepository):

    def list(self) -> List[Notification]:
        notifies: [NotificationDTO] = self.db.query(NotificationDTO).all()
        return list(map(lambda notify: notify.to_entity(), notifies))

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

    def count_total_not_seen(self) -> int:
        return self.db.query(func.count(NotificationDTO.id)). \
            where(NotificationDTO.seen_status == SeenStatus.not_seen).scalar()

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
