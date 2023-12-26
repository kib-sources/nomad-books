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
assert TELEGRAM_TOKEN_ACCESS.replace('*', ''), "Уберите звёздочки из TELEGRAM_TOKEN_ACCESS"

POSTGRES_USER = os.getenv("POSTGRES_USER", "nomad")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", None)
assert POSTGRES_PASSWORD, "Укажите пароль к Postgress POSTGRES_PASSWORD"
assert POSTGRES_PASSWORD.replace('*', ''), "Уберите звёздочки из POSTGRES_PASSWORD"


POSTGRES_DB = os.getenv("POSTGRES_DB", POSTGRES_USER)
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))

# POSTGRES_PRISMA_URL = os.getenv(
#     "POSTGRES_PRISMA_URL", None # "postgresql://<POSTGRES_USER>:<POSTGRES_PASSWORD>@localhost:<POSTGRES_PORT>/mydb?schema=<POSTGRES_DB>"
# )

POSTGRES_SQLALCHEMY_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_PORT}/{POSTGRES_DB}'
POSTGRES_SQLALCHEMY_URL_password_esc = POSTGRES_SQLALCHEMY_URL.replace(POSTGRES_PASSWORD, '********')


# POSTGRES_URL = POSTGRES_URL.\
#     replace('<POSTGRES_USER>', POSTGRES_USER).\
#     replace("<POSTGRES_PASSWORD>", POSTGRES_PASSWORD).\
#    replace('<POSTGRES_PORT>', str(POSTGRES_PORT)).\
#    replace('<POSTGRES_DB>', POSTGRES_DB)