from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import get_settings

SQLALCHEMY_DATABASE_URL = get_settings().DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine,
)

SessionLocal.configure(bind=engine)
Base = declarative_base()


def create_tables():
    Base.metadata.create_all(bind=engine)
