"""
<nomad-books>
/settings.py
    create by pavelmstu in 16.10.2023
--------------------------------------------------------

Общие настройки переменных окружения

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


API_HOST = os.getenv('API_HOST', '0.0.0.0')

# При смене порта, не забудьте поменять его в docker-compose.yaml
# https порт по умолчанию
API_PORT = int(os.getenv('API_PORT', 443))

SSL_KEYFILE_PASSWORD = os.getenv('SSL_KEYFILE_PASSWORD', None)

ORGANIZATION = os.getenv('ORGANIZATION', "Клуб Информационной Безопасности")