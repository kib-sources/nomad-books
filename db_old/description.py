"""
<nomad-books>
db_old/descriptions.py
    create by pavelmstu in 14.10.2023
--------------------------------------------------------

Описания книг

Описание экземпляров книг см. в db_old.sample

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

__version__ = "20231014"
__status__ = "Development"

# __status__ = "Production"

import os
import enum
from sqlalchemy import Enum
from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean, BigInteger
from sqlalchemy import ARRAY

from db_old.base import Base


class DescriptionType(enum.Enum):
    undef = 'undef'
    #
    article = 'article'
    book = 'book'
    booklet = 'booklet'
    conference = 'conference'
    inbook = 'inbook'
    incollection = 'incollection'
    inproceedings = 'inproceedings'
    manual = 'manual'
    mastersthesis = 'mastersthesis'
    misc = 'misc'
    phdthesis = 'phdthesis'
    proceedings = 'proceedings'
    techreport = 'techreport'
    unpublished = 'unpublished'

    #
    reserved1 = 'reserved1'
    reserved2 = 'reserved2'
    reserved3 = 'reserved3'
    reserved4 = 'reserved4'
    reserved5 = 'reserved5'


class Description(Base):
    """
    Описание книг.

    По неймингу следует придерживатся BibTeX
    https://ru.wikipedia.org/wiki/BibTeX
    """
    __tablename__ = 'description'

    # id = Column(Integer, primary_key=True)
    id = Column(BigInteger, primary_key=True)

    type = Column(Enum(DescriptionType), comment="Тип издания")
    title = Column(String, comment="Заголовок")
    year = Column(Integer, comment='год издания')
    month = Column(Integer, comment='месяц издания (если указан)', default=None)
    day = Column(Integer, comment='день издания (если указан)', default=None)
    author = Column(String, comment="Автор или список авторов, разделённый ';'")
    publisher = Column(Integer, comment="Издатель")
    pages = Column(Integer, comment="Общее количество страниц")
    address = Column(String, comment=" Адрес издателя (обычно просто город, но может быть полным адресом для малоизвестных издателей)" )
    isbn = Column(String, comment="Код издания ISBN (Международный стандартный книжный номер)")
    lang = Column(String, comment="Язык или языки, разделённые ';'. Например 'ru;en'")

    edition = Column(String, comment=" Издание (полная строка, например, '1-е, стереотипное'", default=None)
    journal = Column(String, comment='Название журнала', default=None)
    number = Column(String, comment='Номер журнала', default=None)

    image_cover = Column(BigInteger, nullable=True, comment="image.id обложки")
    images = Column(ARRAY(BigInteger), nullable=True, comment="Произвольные изображения")