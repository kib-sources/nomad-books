"""
models.base

Базовые классы

Create at 26.12.2023 15:44:07
~/models/base.py
"""

__author__ = 'pavelmstu'
__copyright__ = 'KIB, 2023'
__license__ = 'KIB'
__credits__ = [
    'pavelmstu',
]
__version__ = "20231226"
__status__ = 'Develop'

import datetime
# __status__ = "Production"

import uuid

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped as _Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, ForeignKey

from sqlalchemy import Column
from sqlalchemy import String, Integer, UUID, DateTime, BLOB

from sqlalchemy.sql import func

Mapped = _Mapped


def new_id():
    return uuid.uuid4()


def _onupdate_update_at(context):
    return datetime.datetime.utcnow()


class BaseModel(MappedAsDataclass, DeclarativeBase):
    """Базовый класс"""

    id = Column(UUID, primary_key=True, default=new_id, comment="Уникальный UUID записи.")

    create_at = Column(DateTime, default=datetime.datetime.utcnow, comment="время создания записи в таблице")

    update_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=_onupdate_update_at, comment="время последнего изменения данной записи")

    comment = Column(String, default=None, comment="Произвольный комментарий к строке")

    @classmethod
    def make(cls, **kwargs):
        obj = cls()
        for key, value in kwargs.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
            else:
                raise ValueError(f"Нет поля {key} для класса {cls.__name__}")
        return obj

