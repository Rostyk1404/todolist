from configparser import ConfigParser
import jwt


class SecretFile:
    @classmethod
    def secret_key_getter(cls):
        conf_file = ConfigParser()
        conf_file.read("full path to file with filename")
        secret_key = (conf_file.get("Secret Word", "secret_word"))
        jwt_secret_key = jwt.encode({}, secret_key, algorithm='HS256').decode()
        return jwt_secret_key
