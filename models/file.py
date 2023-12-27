"""
class Files(BaseModel)

Create at 26.12.2023 15:42:49
~/models/file.py
"""

__author__ = 'pavelmstu'
__copyright__ = 'KIB, 2023'
__license__ = 'KIB'
__credits__ = [
    'pavelmstu',
]
__version__ = "20231226"
__status__ = 'Develop'

# __status__ = "Production"

# from sqlalchemy.orm import mapped_column
from sqlalchemy import Column
from sqlalchemy import Unicode, Integer, UUID, DateTime, LargeBinary
from models.base import BaseModel, new_id


# TODO при расширении проекта заменить BLOB на хранилище изображений. Например s3.
class File(BaseModel):
    __tablename__ = "file"
    __table_args__ = {
        'comment': 'BLOB хранилище всех фотографий и иных файлов.'
    }
    # id, create_at, update_at, comment,

    # sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedObject) type "blob" does not exist
    # body = Column(BLOB, default=None, comment=
    body = Column(LargeBinary, default=None, comment='бинарные данные файла')

    name = Column(Unicode, default=None, comment="(опционально) имя файла с расширением. Например 'some.png'")

    type = Column(Unicode, nullable=False, comment="расширение файла в нижнем регистре. Например png")
