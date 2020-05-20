from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, String, Integer
from models.base import Base, scoped_session


class Users(Base):
    __tablename__ = 'users'
    users_id = Column(Integer, autoincrement=True, primary_key=True)
    email = Column(String(50), index=True, unique=True)
    password_hash = Column(String(128))
    username = Column(String(25), index=True, unique=True)
    token_field = Column(String)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.users_id}/{self.email}/{self.username}>"

    @classmethod
    def logout(cls):
        with scoped_session() as session:
            session.close()

    @classmethod
    def get_user_by_email(cls, email):
        with scoped_session() as session:
            return session.query(Users).filter_by(email=email).first()

    @classmethod
    def get_user_by_id(cls, users_id):
        with scoped_session() as session:
            return session.query(Users).filter_by(users_id=users_id).first()

    @classmethod
    def get_user_by_username(cls, username):
        with scoped_session() as session:
            return session.query(Users).filter_by(username=username).first()

    @classmethod
    def get_all_users(cls):
        with scoped_session() as session:
            return session.query(Users).all()

    @classmethod
    def registation_user(cls, email, username, password):
        """
        :param email:
        :param password:
        :param username:
        :return:
        """
        with scoped_session()as session:
            user = Users(email=email, username=username)
            user.set_password(password)
            session.add(user)
        return user

    @classmethod
    def update_user_by_email(cls, email, token_field):
        with scoped_session() as session:
            user = session.query(Users).filter_by(email=email).update({"token_field": token_field})
        return user

    @classmethod
    def update_user(cls, users_id, user_data):
        with scoped_session() as session:
            user = session.query(Users).filter_by(users_id=users_id).one()
            for k, v in user_data.items():
                setattr(user, k, v)
            return user

    # @classmethod
    # def logout(cls):
    #     with scoped_session() as session:
    #         if Users.token_field is not "":
    #
    #     session.close()

    @classmethod
    def update_password(cls, users_id, password):
        with scoped_session() as session:
            new_password = generate_password_hash(password)
            return session.query(Users).filter_by(users_id=users_id).update({"password_hash": new_password})

    @classmethod
    def delete_user(cls, users_id):
        with scoped_session() as session:
            return session.query(Users).filter_by(users_id=users_id).delete()

    @classmethod
    def delete_all_users(cls):
        with scoped_session() as session:
            return session.query(Users).delete()

# if __name__ == "__main__":

#
#     Users.registation_user(email="novosiadlo@gmail.com", password="123456789", username="tarzan")
# Users.update_email(users_id=1, email="2324578asd")
# sers.update_password(users_id=1, password="2324578a")U
# Tasks.create_task(task_name="sleep", user_id=1)
# Tasks.update_task(task_id=1, task_name="lox")
# Tasks.delete_task(task_id=1)
# user = Users(email='ross.novos@gmail.com', password="23132", token="wearethechampion")
