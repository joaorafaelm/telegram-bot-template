import logging
import os
import sys

import dj_database_url

from pydantic import BaseSettings, PyObject


class Conf(BaseSettings):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DEBUG: bool = False
    DATABASES = {"default": dj_database_url.config()}
    INSTALLED_APPS = ("bot",)
    SECRET_KEY: str = "secret"
    LOG_LEVEL: PyObject = "logging.INFO"
    TELEGRAM_TOKEN: str = ...

    class Config:
        env_prefix = ''


# expose attributes to module scope for django compatibility
*map(lambda x: setattr(sys.modules[__name__], *x), Conf().dict().items()),
