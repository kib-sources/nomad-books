"""
class Sample(BaseModel)

Create at 28.12.2023 17:22:46
~/models/sample.py
"""

__author__ = 'pavelmstu'
__copyright__ = 'KIB, 2023'
__license__ = 'KIB'
__credits__ = [
    'pavelmstu',
]
__version__ = "20231228"
__status__ = 'Develop'

# __status__ = "Production"

import os

from typing import Any


from models.base import BaseModel, new_id

import enum
from sqlalchemy import Column
from sqlalchemy import UUID, Enum, Unicode, UnicodeText, SmallInteger, BigInteger, ARRAY, Boolean


class SampleStatus(enum.Enum):
    """
    Статус экземпляра книги
    """

    # Книга создана
    init = "init"

    # Книга выгружена в A4 наклейки её создателю.
    # Создатель экземпляра ещё не подтвердил, что наклеил QR код.
    pulled = "pulled"

    # Книга у владельца.
    active = 'active'

    # Книга потеряна или испорчена
    lost = 'lost'

    # Особый статус для разработчиков.
    # Книга заблокирована для каких-либо исследований... Но она не потеряна
    block = "block"

    reserved1 = 'reserved1'
    reserved2 = 'reserved2'
    reserved3 = 'reserved3'


class SampleReadingStatus(enum.Enum):
    """
    Статус читателя экземпляра книги
    """

    # Книга ОЧЕНЬ нужна.
    exam = -2

    # Книга в активном чтении
    active_reading = -1

    # Книга читается более-менее.
    passive_reading = 1

    # Книга не нужна владельцу, он готов её отдать.
    free = 2

    # Пользователь хочет выйти из движения
    # и нужно собрать все книги у него как можно скорее
    zombie_user = 3


class Sample(BaseModel):
    __tablename__ = "sample"
    __table_args__ = {
        'comment': 'Экземпляр конкретной книги.'
    }

    description_id = Column(UUID, index=True, nullable=False,
                            comment="Ссылка на Description.id. Описание книги, для которого есть этот экземпляр.")
    user_id_create = Column(BigInteger, index=False, nullable=False,
                            comment="Пользователь Telegram, создавший данный экземпляр.")
    user_id_owner = Column(BigInteger, index=True, nullable=False,
                           comment="Текущий ответственный за данную книгу.")

    status = Column(Enum(SampleStatus), nullable=False,
                    comment="Статус экземпляра книги")
    reading_status = Column(Enum(SampleReadingStatus), default=SampleReadingStatus.passive_reading,
                            comment="Как активно читается книга текущим владельцем")

    lost_comment = Column(UnicodeText, nullable=True, default=None,
                          comment="Если книга потеряна, то комментарий о решении по потере")

    # enabled = Column(Boolean, default=False,
    #                  comment="Если False, то экземпляр книги ещё недоступен")

    # def __init__(self, **kw: Any):
    #     super().__init__(**kw)