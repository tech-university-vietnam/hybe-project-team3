from sqlalchemy.orm import Session

from app.infrastructure.postgresql.database import session


class DatabaseRepository:
    def __init__(self):
        self.db: Session = session
