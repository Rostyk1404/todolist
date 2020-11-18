import os
from postgres_helper.postgres_config import HOST, PORT, POSTGRES_PASSWORD, POSTGRES_USER, USER_DB

BASEDIR = os.path.abspath(os.path.dirname(__file__))

"""
    This is a config class for user_service
"""


class Config:
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{HOST}:{PORT}/{USER_DB}"
