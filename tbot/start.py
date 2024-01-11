"""
core.auth

Функции аутентификации

Create at 21.12.2023 20:02:52
~/core/start.py
"""

__author__ = 'pavelmstu'
__copyright__ = 'KIB, 2023'
__license__ = 'KIB'
__credits__ = [
    'pavelmstu',
]
__version__ = "20231221"
__status__ = 'Develop'

import datetime

# __status__ = "Production"


from tbot import bot

from tbot.common import get_active_user

from settings import USER_OWNER_ID

from settings import INVITE_LIFETIME_MIN

from models.user import User


def _get_user_by_username(username) -> User:
    pass


@bot.message_handler(commands=["start"])
def start(message, res=False):

    if message.from_user.is_bot:
        # с ботами никак не взаимодействуем.
        return

    user_id = message.from_user.id
    username = message.from_user.username
    user = get_active_user(user_id)

    if user is None:
        # Возможно три варианта:
        # 1) этот пользователь OWNER
        # 2) этот пользователь получил invite и его user_id записан отрицательным числом
        # 3) это посторонний пользователь и его нужно проигнорировать.
        if user_id == USER_OWNER_ID:
            pass
        else:
            user = _get_user_by_username(username)
            if datetime.datetime.now() > user.update_at + datetime.timedelta(minutes=INVITE_LIFETIME_MIN)


    bot.send_message(
        message.chat.id,
        'Я на связи! Напиши мне что-нибудь ) ',
        parse_mode='HTML',
    )