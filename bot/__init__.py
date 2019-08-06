import logging
import os

import django
from bot import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bot.settings")
django.setup()
logging.basicConfig(level=settings.LOG_LEVEL)
