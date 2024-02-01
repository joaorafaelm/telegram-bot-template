import dj_database_url

from pydantic import PyObject
from pydantic_settings import BaseSettings


class Conf(BaseSettings):
    DEBUG: bool = False
    DATABASES: dict = {"default": dj_database_url.config()}
    INSTALLED_APPS: tuple = ("bot",)
    SECRET_KEY: str = "secret"
    LOG_LEVEL: PyObject = "logging.INFO"
    TELEGRAM_TOKEN: str = ...
    USE_TZ: bool = True


config = Conf()
