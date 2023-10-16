"""
<nomad-books>
db/sample.py
    create by pavelmstu in 15.10.2023
--------------------------------------------------------

Описание конкретный экземпляров книг.

Описание книг -- см. в db.descriptions

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

__version__ = "20231015"
__status__ = "Development"

# __status__ = "Production"

import enum
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean, BigInteger, UUID

from db.base import Base

from db.description import Description
from db.user import User

_description_id = f"{Description.__tablename__}.id"
_user_id = f"{User.__tablename__}.id"


class SampleStatus(enum.Enum):
    undef = 'undef'
    #

    # Активное чтение.
    # Книга не показывается в поиске.
    # раз в 48 часов нужно обновлять статус.
    active_reading = 'active_reading'

    # Книга у владельца.
    # Владелец её не освободил
    reading = 'reading'

    # Книга у владельца.
    # Владельцу она не нужна, он готов её отдать
    free = 'free'

    # Книга потеряна
    lost = 'lost'

    # Книга испорчена
    vandal = 'vandal'


class Sample(Base):
    """
    Экземпляры книг
    """
    __tablename__ = 'sample'

    # id = Column(Integer, primary_key=True)
    id = Column(BigInteger, primary_key=True)
    uuid = Column(UUID, nullable=False)

    description_id = Column(BigInteger, ForeignKey(_description_id, nullable=False))
    user_id = Column(BigInteger, ForeignKey(_user_id, nullable=False))

    status = Column(Enum(SampleStatus), comment="Статус экземпляра книги")

    lost_comment = Column(String, comment="Если книга потеряна, то комментарий о решении по потере")

    comment = Column(String, comment="произвольный комментарий")


