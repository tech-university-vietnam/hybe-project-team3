from app.domains.notification.notification_repository import NotificationRepository


class NotificationService:

    def __init__(self, notification_repository: NotificationRepository):
        self.notification_repo = notification_repository

    def create(self, data):
        return self.notification_repo.create(data)

    def list(self):
        return self.notification_repo.list()

    def update(self, data, source_id, user_id):
        return self.notification_repo.update(data, source_id, user_id)

    def _is_created_by_user(self, user_id):
        return self.notification_repo.check_user_id(user_id)

    def delete(self, id, user_id):
        """
        If user has the same id as created_by id -> delete
        If not -> check if user is in the same id
        """
        try:
            return self.notification_repo.delete(id, user_id)
        except:
            raise PermissionError
