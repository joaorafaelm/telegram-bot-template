import mock
import pytest
from bot.__main__ import messages, start

pytestmark = pytest.mark.django_db


@pytest.fixture
def mock_bot():
    with mock.patch("bot.__main__.bot") as mock_bot:
        yield mock_bot


@pytest.fixture
def message():
    class message:
        text = "dummy"

        class chat:
            id = 1

    return message


def test_start(mock_bot, message):
    start(message)
    assert mock_bot.send_message.called is True


def test_messages(mock_bot, message):
    messages(message)
    assert mock_bot.send_message.called is True
