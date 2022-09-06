
import pinject
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings
from app import register_spec

_Session = None
ClientClass = None
Base = None
_engine = None
SQLALCHEMY_DATABASE_URL = get_settings().DATABASE_URL


class AsyncSessionBindingSpec(pinject.BindingSpec):
    @pinject.provides(in_scope=pinject.PROTOTYPE)
    def provide_session(self):
        return _Session()


def init_db(show_logs=True, test=False):
    global _engine
    _engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True if show_logs is True else False)
    global _Session
    _Session = sessionmaker(bind=_engine)
    register_spec(AsyncSessionBindingSpec())
    global Base
    Base = declarative_base()
    if test:
        Base.metadata.drop_all(bind=_engine)
        Base.metadata.create_all(bind=_engine)


def drop_db():
    Base.metadata.drop_all(bind=_engine)


def session_scope():
    global _Session
    session = _Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
