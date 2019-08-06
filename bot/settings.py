import logging
import os

from decouple import config
from dj_database_url import parse as parse_db_url

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEBUG = config("DEBUG", default=False, cast=bool)
DATABASES = {"default": config("DATABASE_URL", cast=parse_db_url)}
INSTALLED_APPS = ("bot",)
SECRET_KEY = config("SECRET_KEY", default="secret")
LOG_LEVEL = config("LOG_LEVEL", default="INFO", cast=logging.getLevelName)
TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
