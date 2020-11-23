from sqlalchemy import Column, String, Integer, ForeignKey
from app.database import scoped_session
from app.models import Base
from app.models.user import Users
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields


class Tasks(Base):
    __tablename__ = "tasks"
    task_id = Column(Integer,
                     autoincrement=True, primary_key=True)
    task_name = Column(String(180))
    user_id = Column(Integer, ForeignKey(Users.users_id))
    user = relationship(Users)

    @classmethod
    def create_task(cls, task_name, user_id):
        with scoped_session() as session:
            tasks = Tasks(task_name=task_name, user_id=user_id)
            session.add(tasks)

    @classmethod
    def get_task_by_id(cls, task_id):
        with scoped_session() as session:
            return session.query(Tasks).filter_by(task_id=task_id).first()

    @classmethod
    def get_task_by_name(cls, task_name):
        with scoped_session() as session:
            return session.query(Tasks).filter_by(task_name=task_name).first()

    @classmethod
    def get_all_tasks(cls):
        with scoped_session() as session:
            return session.query(Tasks).all()

    @classmethod
    def update_task(cls, task_id, task_data):
        with scoped_session() as session:
            task = session.query(Tasks).filter_by(task_id=task_id).one()

            for k, v in task_data.items():
                setattr(task, k, v)
            return task

    @classmethod
    def delete_task(cls, task_id):
        with scoped_session() as session:
            return session.query(Tasks).filter_by(task_id=task_id).delete()

    @classmethod
    def delete_all_task(cls):
        with scoped_session() as session:
            return session.query(Tasks).delete()


class TaskSchema(Schema):
    task_id = fields.Integer(required=True)
    task_name = fields.String(required=True)
    user_id = fields.Integer(required=True)
