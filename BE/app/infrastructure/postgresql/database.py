from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:example@localhost:5432/postgres"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

SessionLocal.configure(bind=engine)
session: Session = SessionLocal()

Base = declarative_base()


def create_tables():
    Base.metadata.create_all(bind=engine)
