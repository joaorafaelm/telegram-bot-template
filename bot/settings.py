import dj_database_url

from typing import Dict
from pydantic import ImportString
from pydantic_settings import BaseSettings


class Conf(BaseSettings):
    DEBUG: bool = False
    DATABASES: Dict = {"default": dj_database_url.config()}
    INSTALLED_APPS: tuple = ("bot",)
    SECRET_KEY: str = "secret"
    LOG_LEVEL: ImportString = "logging.INFO"
    TELEGRAM_TOKEN: str = ...
    USE_TZ: bool = True


config = Conf()
