from sqlalchemy.orm import Session

from abc import ABC


class DatabaseRepository(ABC):
    def __init__(self, session):
        self.session = session

    @property
    def db(self) -> Session:
        return self.session
