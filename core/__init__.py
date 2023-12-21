"""
Ядро системы телеграмм-бота

Create at 21.12.2023 19:50:06
~/core/__init__.py
"""

__author__ = 'pavelmstu'
__copyright__ = 'KIB, 2023'
__license__ = 'KIB'
__credits__ = [
    'pavelmstu',
]
__version__ = "20231221"
__status__ = 'Develop'

# __status__ = "Production"

import telebot

from settings import TELEGRAM_USERNAME, TELEGRAM_TOKEN_ACCESS

bot = telebot.TeleBot(TELEGRAM_TOKEN_ACCESS)

