from typing import Iterator

from app.domains.notification.notification_repository import NotificationRepository
from app.model.notification import Notification


class NotificationService:

    def __init__(self, notification_repository: NotificationRepository):
        self.notify_repo = notification_repository

    def list(self):
        return self.notify_repo.list()

    def create(self, payload: Notification):
        return self.notify_repo.create(payload)

    def approved(self, id: int):
        return self.notify_repo.approved(id)

    def declined(self, id: int):
        return self.notify_repo.declined(id)

    def count_total_not_seen(self):
        return self.notify_repo.count_total_not_seen()

    def update_all_seen_status(self, ids: Iterator[int]):
        return self.notify_repo.update_all_seen_status(ids)
