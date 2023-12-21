"""
Запускаемый файл

Create at 21.12.2023 19:46:51
~/run.py
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

import os

# ---------------------------------------------------------------------------------------------------------------------
# Инициализация всех функций.
import core.auth  # !
# ---------------------------------------------------------------------------------------------------------------------
import sys
import logging
from time import sleep
from core import bot

from settings import TELEGRAM_USERNAME

# Запись логов в консоль.
logging.basicConfig(level=logging.DEBUG)


def main():

    while True:
        pool_count = 1
        try:
            # ---------------------------------------------------------------------------------------------------------
            # Запуск бота.
            print("logging....")

            logging.info(f"Запуск бота @{TELEGRAM_USERNAME}. pool_count={pool_count}")
            bot.polling(none_stop=True, interval=0)
            # ---------------------------------------------------------------------------------------------------------
        except Exception as e:
            # TODO сообщение об ошибке пулинга
            pool_count += 1
            logging.error("Ошибка в bot.polling. ")
            sleep(10)
            continue


if __name__ == "__main__":
    main()
