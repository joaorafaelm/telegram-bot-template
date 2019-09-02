import telebot
from bot.settings import config

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)
