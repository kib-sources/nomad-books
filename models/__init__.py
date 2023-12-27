"""
Общий файл для импортирования

from models import File

Create at 26.12.2023 15:43:15
~/models/__init__.py
"""

__author__ = 'pavelmstu'
__copyright__ = 'KIB, 2023'
__license__ = 'KIB'
__credits__ = [
    'pavelmstu',
]
__version__ = "20231226"
__status__ = "Production"

import os

import logging

from models.base import BaseModel

# ---------------------------------------------------------------------------------------------------------------------
from models.file import File
from models.description import Description
# ---------------------------------------------------------------------------------------------------------------------

from settings import POSTGRES_SQLALCHEMY_URL, POSTGRES_SQLALCHEMY_URL_password_esc

from sqlalchemy import text
from sqlalchemy import create_engine

try:
    engine = create_engine(
        POSTGRES_SQLALCHEMY_URL,
        echo=True
    )
except Exception as e:
    logging.fatal(f"Некорректный POSTGRES_SQLALCHEMY_URL={POSTGRES_SQLALCHEMY_URL_password_esc}")
    raise e


def test_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT datname FROM pg_database;"))
    except Exception as e:
        return False
    else:
        return True


def init():
    """
    Инициализировать всё
    :return:
    True -- корректно
    False -- ошибка при инициализации
    """
    if not test_connection():
        logging.fatal(f"Некорректный POSTGRES_SQLALCHEMY_URL={POSTGRES_SQLALCHEMY_URL_password_esc}, или база данных не поднята")
        return False

    # create_tables
    # Files.__table__.create(engine, checkfirst=True)
    # ...
    BaseModel.metadata.create_all(engine)

    return True