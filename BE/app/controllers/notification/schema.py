from datetime import datetime
from typing import Optional

from app.model.notification import Notification


class NotificationPayload(Notification):
    id: Optional[int]
    created_at: Optional[datetime]
