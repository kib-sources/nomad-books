"""
Стандартные ошибки, выдаваемые ботом.

Create at 09.01.2024 18:45:59
~/tbot/errors.py
"""

__author__ = 'pavelmstu'
__copyright__ = 'KIB, 2024'
__license__ = 'KIB'
__credits__ = [
    'pavelmstu',
]
__version__ = "20240109"
__status__ = "Production"


class NomadError(Exception):
    pass


class NomadDataExistsError(Exception):
    """
    Ошибка в консистентности данных
    """
    pass

