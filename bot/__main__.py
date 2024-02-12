import logging

from bot.clients import bot
from bot.flights import get_explore_flights

logger = logging.getLogger(__name__)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "hi")


@bot.message_handler(commands=["explore"])
def explore(message):
    flights = get_explore_flights()
    bot.send_message(message.chat.id, flights)


@bot.message_handler(func=lambda x: x)
def messages(message):
    logger.info(f"message: {message.text}")
    bot.send_message(message.chat.id, message.text)


if __name__ == "__main__":
    logger.info("running")
    bot.polling()
