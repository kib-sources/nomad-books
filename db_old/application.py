"""
<nomad-books>
db_old/application.py
    create by pavelmstu in 16.10.2023
--------------------------------------------------------

db_old.application -- описание таблицы данных приложения

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
from sqlalchemy import ARRAY

from db_old.base import Base

from db_old.description import Description

from db_old.user import User

_user_id = f"{User.__tablename__}.id"




class ApplicationStatus(enum.Enum):
    undef = 'undef'
    #

    not_authorized = "not_authorized"

    authorized = "authorized"

    blocked = 'blocked'


    #
    reserved1 = 'reserved1'
    reserved2 = 'reserved2'
    reserved3 = 'reserved3'
    reserved4 = 'reserved4'
    reserved5 = 'reserved5'


class Application(Base):
    """
    Пользователь системы
    Nomad Books
    """
    __tablename__ = 'user'

    # id = Column(Integer, primary_key=True)
    id = Column(BigInteger, primary_key=True)
    uuid = Column(UUID)

    user_id = Column(BigInteger, ForeignKey(_user_id, nullable=False))

    status = Column(Enum(ApplicationStatus), comment="статус приложения")

    rsa_pub = Column(String, comment="RSA публичный ключ")
