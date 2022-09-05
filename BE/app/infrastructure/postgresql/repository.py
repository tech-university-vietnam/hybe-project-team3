from sqlalchemy.orm import Session


class DatabaseRepository:
    def __init__(self, session: _Session):
        self.db: _Session = session
