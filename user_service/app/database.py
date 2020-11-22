""" This module exports the database engine.
Notes:
     Using the scoped_session contextmanager is
     best practice to ensure the session gets closed
     and reduces noise in code by not having to manually
     commit or rollback the db if a exception occurs.
"""
import os
import time
from alembic import command
from alembic.config import Config
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError, OperationalError as SQLAlchemyConnectionError
# from app_config import DATABASE_URL
from postgres_helper.postgres_config import HOST, PORT, POSTGRES_PASSWORD, POSTGRES_USER, USER_DB

ENGINE = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{HOST}:{PORT}/{USER_DB}")

# Session to be used throughout app.cd
Session = sessionmaker(bind=ENGINE, expire_on_commit=False)

RETRIES = 30
while True:
    try:
        # declare connection
        CONNECTION = ENGINE.connect()
        break
    except SQLAlchemyConnectionError as exc:
        if RETRIES == 0:
            print('Failed to connect!')
            raise exc
        RETRIES -= 1
        time.sleep(1)
print('Successfully connected!')
CONNECTION.close()


@contextmanager
def scoped_session():
    session = Session()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close()


# run migrations
# ALEMBIC_INI_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'alembic.ini')
# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
# print(ALEMBIC_INI_FILE)
# # path to alemic.ini file
# ALEMBIC_CONFIG = Config(ALEMBIC_INI_FILE)
# command.upgrade(ALEMBIC_CONFIG, "head")
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!