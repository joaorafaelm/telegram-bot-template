import logging
import os

import django
from bot import settings

# expose attributes to module scope to maintain django compatibility
*map(lambda x: setattr(settings, *x), settings.config.dict().items()),

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bot.settings")
django.setup()
logging.basicConfig(level=settings.config.LOG_LEVEL)
