from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


def import_models():
    from app.infrastructure.postgresql.user.user_dto import UserDTO

    return [UserDTO]
