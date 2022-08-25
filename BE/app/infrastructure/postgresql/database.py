from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = ("postgresql://postgres:password@database:5432/" +
                           "postgres")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)

SessionLocal = sessionmaker(
    bind=engine,
)

SessionLocal.configure(bind=engine)
session: Session = SessionLocal()

Base = declarative_base()


def create_tables():
    Base.metadata.create_all(bind=engine)
