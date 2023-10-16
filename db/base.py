"""
<nomad-books>
db/base.py
    create by pavelmstu in 14.10.2023
--------------------------------------------------------

TODO подробное описание, что это за файл

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
__status__ = "Production"

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()