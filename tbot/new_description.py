"""
Функции по работе с книгами:
* descriptions
* samples

Create at 26.12.2023 18:47:39
~/tbot/description.py
"""

__author__ = 'pavelmstu'
__copyright__ = 'KIB, 2023'
__license__ = 'KIB'
__credits__ = [
    'pavelmstu',
]
__version__ = "20231227"
__status__ = 'Develop'

# __status__ = "Production"


from sqlalchemy.orm import Session

from tbot import bot

from models import Description
from models import engine

# chat_id -> context
_context_dict = dict()
# chat_id -> timestamp. Нужно для удаления старых записей
_context_timestamp_dict = dict()


def  _break_step(message):
    _ = bot.send_message(
        message.chat.id,
        f'''Вы отменили операцию\\. Введите `\\new-description` повторно для создания нового описания.
        ''',
        parse_mode='MarkdownV2',
    )

def _timeout_step(message):
    _ = bot.send_message(
        message.chat.id,
        f'''Прошло слишком много времени\\. Контекст вычищен\\. Начните сначала\\!
        ''',
        parse_mode='MarkdownV2',
    )


def _error_field_step(message, field_name, field_value):
    _ = bot.send_message(
        message.chat.id,
        f'''Некорректное поле `{field_name}`\\="{field_value}"\\. Начните сначала
        ''',
        parse_mode='MarkdownV2',
    )


def _get_array(array_str):
    return [v.strip() for v in array_str.split(',')]


def _one_step(message, field, field_map_func, next_text, next_func, optional=True):
    global _context_dict
    chat_id = message.chat.id
    context = _context_dict.get(chat_id)
    if context is None:
        return _timeout_step(message)

    value = message.text
    if value.lower() in [
        "break",
        "отмена",
        "\\q",
    ]:
        return _break_step(message)
    try:
        if value == '-' and optional:
            value = None
        else:
            value = field_map_func(value)
    except:
        return _error_field_step(
            message,
            field,
            value,
        )
    context[field] = value

    # запрашиваем about
    message_next = bot.send_message(
        message.chat.id,
        next_text,
        parse_mode='MarkdownV2',
    )
    bot.register_next_step_handler(message_next, next_func)


def _end_step(message):
    global _context_dict
    chat_id = message.chat.id
    context = _context_dict.get(chat_id)
    if context:
        # удаляем контекст
        _context_dict.pop(chat_id)

    context['comment'] = message.text

    description = Description.make(**context)

    with Session(engine) as session:
        session.add(description)
        session.commit()
        session.refresh(description)

    bot.send_message(
        message.chat.id,
        f"""Добавлено описание книги **"{description.full_title()}"**
id\\=`{description.id}`

Для добавления экземпляров книги введите команду:
```
\\new_samples {description.id} --count N
```
где вместо `N` должно быть количество экземпляров\\.
""",
        parse_mode='MarkdownV2',
    )


def _step99(message):
    _one_step(
        message,
        'tags',
        _get_array,
        f'''Введите произвольный комментарий для разработчиков \n \\(Опционально, ставьте `-` если не нужно\\)
        ''',
        _end_step
    )


def _step6(message):
    _one_step(
        message,
        'authors',
        _get_array,
        f'''Введите теги **через запятую** \n одним сообщением \\.
        ''',
        _step99
    )


def _step5(message):
    _one_step(
        message,
        'about',
        str,
        f'''Введите всех авторов **через запятую** \n одним сообщением \\.
        ''',
        _step6
    )


def _step4(message):
    _one_step(
        message,
        'year',
        int,
        f'''Введите **подробное** описание\\. \n одним сообщением\\.
        ''',
        _step5,
        optional=False,
    )


def _step3(message):
    _one_step(
        message,
        'number',
        int,
          f'''Введите год издания\\. \n ОБЯЗАТЕЛЬНОЕ поле\\.
        ''',
        _step4
    )


def _step2(message):
    _one_step(
        message,
        'title',
        str,
        f'''Введите номер журнала, например `3(45)` 
           или версию издания текстом, например `издание второе`
           ''',
        _step3
    )


@bot.message_handler(commands=["new_description"])
def new_description(m, res=False):
    """
    Регистрация нового описания книги
    """
    global _context_dict
    bot.send_message(
        m.chat.id,
        f'''Новая регистрация книги\\. 
Для этого нужно последовательно ввести ряд полей\\. Следуйте указаниям бота\\.

Введите `break` или `отмена` чтобы остановить процесс\\.
Введите `-` чтобы заполнить поле как None\\.
    ''',
        parse_mode='MarkdownV2',
    )

    message_next = bot.send_message(
        m.chat.id,
        '''Введите название книги (`title`)
'''
    )

    _context_dict[m.chat.id] = dict()

    bot.register_next_step_handler(message_next, _step2)
    ''' # TEST
    _context_dict[m.chat.id] = {
        'title': "пример заголовка",
        'year': 2010,
    }
    bot.register_next_step_handler(message_next, _end_step)  # TEST
    # '''

# ---------------------------------------------------------------------------------------------------------------------