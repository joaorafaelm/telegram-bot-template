import logging
import os
import sys

import dj_database_url

from pydantic import BaseSettings, PyObject


class Conf(BaseSettings):
    DEBUG: bool = False
    DATABASES = {"default": dj_database_url.config()}
    INSTALLED_APPS = ("bot",)
    SECRET_KEY: str = "secret"
    LOG_LEVEL: PyObject = "logging.INFO"
    TELEGRAM_TOKEN: str = ...

    class Config:
        env_prefix = ''


config = Conf()
