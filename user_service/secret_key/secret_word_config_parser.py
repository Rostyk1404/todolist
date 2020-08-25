import jwt
from configparser import ConfigParser


class SecretFile:
    @classmethod
    def secret_key_getter(cls):
        conf_file = ConfigParser()
        conf_file.read("/home/ross/todolist/secret.conf")
        secret_key = (conf_file.get("Secret Word", "secret_word"))
        jwt_secret_key = jwt.encode({}, secret_key, algorithm='HS256').decode()
        return jwt_secret_key
