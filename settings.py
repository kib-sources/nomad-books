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

ORGANIZATION = os.getenv('ORGANIZATION', "Клуб Информационной Безопасности")

TELEGRAM_USERNAME = os.getenv('TELEGRAM_USERNAME', None)
assert TELEGRAM_USERNAME, "Вы не задали TELEGRAM_USERNAME переменную окружения"
assert 'bot' in TELEGRAM_USERNAME, f'В TELEGRAM_USERNAME="{TELEGRAM_USERNAME}" нет подстроки "bot". Это не бот телеграмма'
TELEGRAM_USERNAME = TELEGRAM_USERNAME[1:] if TELEGRAM_USERNAME.startswith('@') else TELEGRAM_USERNAME

TELEGRAM_TOKEN_ACCESS = os.getenv('TELEGRAM_TOKEN_ACCESS', None)
assert TELEGRAM_TOKEN_ACCESS, "Вы не задали TELEGRAM_TOKEN_ACCESS переменную окружения"
