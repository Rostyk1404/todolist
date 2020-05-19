from models.tasks import *
from models.user import *
from models.base import db, Base

Base.metadata.create_all(db)
