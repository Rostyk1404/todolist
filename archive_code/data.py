from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

engine = create_engine("postgres://postgres:example@localhost:5432/ross_db")
if not database_exists(engine.url):
    create_database(engine.url)

print(database_exists(engine.url))