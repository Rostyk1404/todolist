from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from app.app_config import Database_URL
Session = sessionmaker(bind=Database_URL)
session = Session()


@contextmanager
def scoped_session():
    session = Session()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as error:
        raise error
    finally:
        session.close()
