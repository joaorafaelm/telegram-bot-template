import logging

from bot.clients import bot

logger = logging.getLogger(__name__)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "hi")


@bot.message_handler(func=lambda x: x)
def messages(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == "__main__":
    logger.info("running")
    bot.polling()
