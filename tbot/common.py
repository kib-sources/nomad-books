"""
tbot.common -- вспомогательные полезные функции.

Create at 29.12.2023 16:58:43
~/tbot/common.py
"""

__author__ = 'pavelmstu'
__copyright__ = 'KIB, 2023'
__license__ = 'KIB'
__credits__ = [
    'pavelmstu',
]
__version__ = "20240110"
__status__ = "Production"

import logging
import telebot
from tbot import bot
from tbot.errors import NomadError

from typing import Union, List, Optional

from sqlalchemy import select, and_

from sqlalchemy.orm import Session

from models import engine

from models.sample import Sample, SampleStatus


from models.user import UserRole, UserStatus
from models.user import User


def get_active_user(*, user_id) -> Optional[User]:

    with Session(engine) as session:

        query = select(User).where(
            and_(User.status == UserStatus.active.value, User.id == user_id)
                 )

        result = session.execute(
            query
        ).one_or_none()

        for _users in result:
            user = _users[0]
            # yield sample
            return user
    return None


def get_samples(user_id_owner, status: SampleStatus):
    samples = list()
    with Session(engine) as session:

        query = select(Sample).where(
            and_(Sample.user_id_owner == user_id_owner, Sample.status == status.value)
                 )

        result = session.execute(
            query
        ).all()

        for _samples in result:
            sample = _samples[0]
            # yield sample
            samples.append(sample)
    return samples


def count_samples(user_id_owner, status: SampleStatus) -> int:
    result = get_samples(user_id_owner, status)
    return len(result)


def grants(role: UserRole):
    """
    Проверка грантов.
    """

    # можно вынести в параметр:
    # def grants(..., status: Union[UserStatus, List[UserStatus]] = UserStatus.active)
    # status = UserStatus.active

    def decorator(func_telebot):

        def inner(message, res=False):
            nonlocal role
            # nonlocal status

            if message.from_user.is_bot:
                # с ботами никак не взаимодействуем.
                pass
                return

            user_id = message.from_user.id
            user = get_active_user(user_id)

            if user is None:
                # Пользователь отсутствует,
                #   либо НЕ активен.

                # В этом случае политика -- бездействие
                pass
                return

            if user.role.value < role.value:
                bot.send_message(
                    message.chat.id,
                    f"""Ваша роль: `{user.role.name}`, нужна роль не ниже `{role.name}`.
Нет прав на данную команду.""",
                    reply_markup=telebot.types.ReplyKeyboardRemove(),
                    parse_mode='HTML',
                )

                return

            # ---------------------------------------------------------------------------------------------------------
            func_telebot(message, res)
            # ---------------------------------------------------------------------------------------------------------

            # logging.info(f"{func_telebot.__name__}: user_id={user_id}", )

            return

        inner.__name__ = func_telebot.__name__
        inner.__doc__ = func_telebot.__doc__
        return inner

    return decorator