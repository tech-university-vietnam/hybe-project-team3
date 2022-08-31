from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.config import get_settings

SQLALCHEMY_DATABASE_URL = get_settings().DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session: Session = SessionLocal()

Base = declarative_base()


def import_models():
    from app.infrastructure.postgresql.user.user_dto import UserDTO

    return [UserDTO]


def create_tables():
    Base.metadata.create_all(bind=engine)
