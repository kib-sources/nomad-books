"""
<nomad-books>
db_old/image.py
    create by pavelmstu in 16.10.2023
--------------------------------------------------------

BLOB хранилище изображений

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
__status__ = "Production"

import os
import enum
from sqlalchemy import Enum
from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean, BigInteger
from sqlalchemy import BLOB

from db_old.base import Base


class Image(Base):
    """
    Изображения
    """
    __tablename__ = 'image'

    id = Column(BigInteger, primary_key=True)
    name = Column(String, comment="наименование файла при загрузке")
    type = Column(String, comment='тип файла при загрузке. Например "png".')

    body = Column(BLOB, comment="изображение в блобе")

    table = Column(String, comment="таблица использования. 'description', 'user' и т.д.")


