"""
core.auth

Функции аутентификации

Create at 21.12.2023 20:02:52
~/core/auth.py
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


from core import bot

@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Я на связи. Напиши мне что-нибудь )')