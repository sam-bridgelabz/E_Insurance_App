import os

from dotenv import load_dotenv

from app.utils.exceptions import RequiredEnvVarError

load_dotenv()


def get_required_env(var_name):
    value = os.getenv(var_name)
    if value is None:
        raise RequiredEnvVarError(var_name)
    return value


class AuthSettings:
    SECRET_KEY = get_required_env("SECRET_KEY")


authSettings = AuthSettings()
