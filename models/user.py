"""
Модуль по работе с пользователями Telegram,
взаимодействующие с ботом.

>> from models.user import User

Create at 09.01.2024 18:56:16
~/models/user.py
"""

__author__ = 'pavelmstu'
__copyright__ = 'KIB, 2024'
__license__ = 'KIB'
__credits__ = [
    'pavelmstu',
]
__version__ = "20240109"
__status__ = 'Develop'
# __status__ = "Production"

import os

from typing import Any


from models.base import BaseModel, new_id

import enum
from sqlalchemy import Column
from sqlalchemy import UUID, Enum, Unicode, UnicodeText, SmallInteger, BigInteger, ARRAY, Boolean

user_owner_id = os.getenv('USER_OWNER_ID', None)


class UserStatus(enum.Enum):

    # Пользователь приглашён, но ещё ни разу не вызвал /start
    invited = 'invited'

    # Пользователь активен.
    # Может брать книги
    active = 'active'

    # Пользователь заблокирован
    blocked = 'blocked'

    # Пользователь хочет выйти из системы,
    # но, возможно, вернул ещё не все книги.
    zombie = 'zombie'

    pass


class UserRole(enum.Enum):

    # Обычный рядовой пользователь
    reader = 10

    # Ментор КИБ-а (например читал ВвС) но без права лидера
    mentor = 20

    # Лидер кружка. Может приглашать других пользователей
    leader = 30

    # Библиотекарь. Может добавлять книги
    librarian = 40

    # Управляющий системой.
    # админ и\или разработчик
    maintainer = 50

    # Владелец системы.
    owner = 60


class User(BaseModel):
    __tablename__ = "user"
    __table_args__ = {
        'comment': 'Пользователь Telegram, зарегистрированный в системе nomad-books'
    }

    # # поле id из BaseModel НЕ используется.
    # # override
    # id = Column(UUID, primary_key=True, default=new_id, comment="Уникальный UUID записи.")
    id = Column(BigInteger, primary_key=True, index=True, nullable=False,
                            comment="Пользователь Telegram. Равен ОТРИЦАТЕЛЬНОМУ значению, если status=invited")

    id_invited_by = Column(BigInteger, index=False, nullable=False,
                       comment="Пользователь Telegram, Давший invite пользователю. Равен 0, если это первоначальный owner")

    bot_chat_id = Column(BigInteger, index=True, default=None,
                     comment="ID чата взаимодействия диалога: бот <-> пользователь.")

    username = Column(Unicode, nullable=False,
                       comment="@username в Telegram системе.")

    status = Column(Enum(UserStatus), nullable=False,
                    comment="Статус пользователя")

    role = Column(Enum(UserRole), nullable=False,
                    comment="Роль пользователя")

