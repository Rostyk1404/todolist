from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from src.helpers.postgres_config_file.postgres_config import HOST, PORT, \
    POSTGRES_PASSWORD, POSTGRES_USER, USER_DB

db = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{HOST}:{PORT}/{USER_DB}")

if not database_exists(db.url):
    create_database(db.url)

Base = declarative_base()

Session = sessionmaker(bind=db)


# session = Session()


@contextmanager
def scoped_session():
    session = Session(expire_on_commit=False)
    try:
        yield session
        session.commit()
    except SQLAlchemyError as error:
        raise error
    finally:
        session.close()
