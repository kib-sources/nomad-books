"""
<nomad-books>
db/user.py
    create by pavelmstu in 16.10.2023
--------------------------------------------------------

Описание пользователей системы.

--------------------------------------------------------
KIB, t.me/kibinfo
"""

__author__ = "pavelmstu"
__license__ = "LGPL"
__copyright__ = "KIB"

__maintainer__ = "pavelmstu"
__email__ = "pavelmstu@yandex.ru"

__credits__ = [
    "pavelmstu",
]

__version__ = "20231016"
__status__ = "Development"

# __status__ = "Production"

import os

import enum
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean, BigInteger, UUID

from db.base import Base

from db.description import Description

_description_id = f"{Description.__tablename__}.id"


class UserRole(enum.Enum):
    """
    Роль пользователя
    """
    undef = 'undef'
    #

    # Обыкновенный рядовой студент
    student = 'student'

    # Рядовой ментор (выпускник, человек из отрасли, читающий факультативы) и т.д.
    mentor = 'mentor'

    # Лидер кружков. Имеет права приглашать других студентов,
    # но несёт моральную отвественность за разъяснение правил работы кочевой библиотеки
    leader = 'leader'

    # Администратор системы. Имеет широкие полномочия по управлению
    admin = 'admin'

    # Управляющий системой. Главный админ и\или разработчик
    maintainer = 'maintainer'

    # Владелец системы
    owner = 'owner'

    #
    reserved1 = 'reserved1'
    reserved2 = 'reserved2'
    reserved3 = 'reserved3'
    reserved4 = 'reserved4'
    reserved5 = 'reserved5'


class UserStatus(enum.Enum):
    """
    Статус пользователя
    """
    undef = 'undef'
    #

    # Пользователь приглашён. Зарегестрирована запись на него.
    # Пользователю нужно написать чат-боту, чат бот вышлет инструкцию и инвайт код.
    invited = 'invited'

    # СТАНДАРТНЫЙ статус
    # 1. пользователь подключил чат-бота
    # 2. пользователь установил приложение
    # 3. пользователь ввёл инвайт
    registered = 'registered'

    # По каким-либо причинам пользователь заблокирован
    # Возможен переход в registered
    blocked = 'blocked'

    # Временный невозвратный статус. Пользователь в процессе удаления из системы
    zombee = 'zombee'

    # Пользователь полностью удалён из системы.
    deleted = 'deleted'

    #
    reserved1 = 'reserved1'
    reserved2 = 'reserved2'
    reserved3 = 'reserved3'
    reserved4 = 'reserved4'
    reserved5 = 'reserved5'


class User(Base):
    """
    Пользователь системы
    Nomad Books
    """
    __tablename__ = 'user'

    # id = Column(Integer, primary_key=True)
    id = Column(BigInteger, primary_key=True)

    # Данные поля отсутствуют, чтобы не попадать в 152 ФЗ о перс.данных
    # name = Column(...
    # soname = Column(...
    # fio = Column(....

    tg_id = Column(String, comment="Телеграмм-аккаунт (id)")
    tg_name = Column(String, comment="Телеграмм-аккаунт (имя)")
    tg_icon_image_id = Column(BigInteger, comment="image.id иконки пользователя в телеграмм-е")

    registration_datetime = Column(DateTime, nullable=False, comment="Время регистрации")

    last_action_datetime = Column(DateTime, comment="Время последнего действия в системе")

    role = Column(Enum(UserRole), comment="Роль пользователя")
    status = Column(Enum(UserStatus), comment="Статус пользователя")

    invite_by_user_id = Column(BigInteger, nullable=True, comment="Каким пользователем приглашён")

    invite_hash_code = Column(String, nullable=True, comment="Если статус invited, то содержит хеш инвайт кода. Иначе Null")

    blocked_comment = Column(String, nullable=True, comment="Если статус blocked, то написана причина заблокированного пользователя")

    comment = Column(String, comment="Произвольный комментарий к пользователю. (Виден только админам и выше)")
