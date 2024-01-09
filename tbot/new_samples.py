"""
Команда /new_samples

Create at 27.12.2023 17:05:00
~/tbot/new_samples.py
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

import os

import uuid

import telebot.types

from sqlalchemy import select, and_

from sqlalchemy.orm import Session

from tbot import bot

from models.description import Description

from models import engine

from models.sample import Sample, SampleStatus

from tbot.common import count_samples

_NO_TEXT = 'Отмена'
_YES_TEXT = "Добавить {N} экземпляров к {description_id}"
assert '{N}' in _YES_TEXT
assert '{description_id}' in _YES_TEXT


def _not_correct_format(message):
    bot.send_message(
        message.chat.id,
        f"""Некорректный формат команды\\. 
    Корректный формат:
    ```
    /new_samples description_id --count N
    ```
    где `description_id` — это UUID описания книги
    а `N` — количество новых экземпляров книги\\.
            """,
        parse_mode='MarkdownV2',
    )
    return


def _not_found_description_id(message, description_id):
    bot.send_message(
        message.chat.id,
        f"""Не найден `description_id`:
```
{description_id}
```
Проверьте\\.""",
        parse_mode='MarkdownV2',
    )
    return


def _step_append_not_correct_input(message):
    _ = bot.send_message(
        message.chat.id,
        f'''Ошибка ввода\\. 
Нужно ввести либо `{_NO_TEXT}`\\, либо `{_YES_TEXT}`''',
        parse_mode='MarkdownV2',
        reply_markup=telebot.types.ReplyKeyboardRemove(),
    )
    return


def _step_append(message):

    # "Отмена"
    # "Добавить {N} экземпляров к {description_id}"
    text = message.text
    user_id = message.from_user.id

    if text == _NO_TEXT:
        _ = bot.send_message(
            message.chat.id,
            f'''Отмена''',
            parse_mode='MarkdownV2',
            reply_markup=telebot.types.ReplyKeyboardRemove(),
        )
        return

    if len(text.split(' ')) != len(_YES_TEXT.split(' ')):
        return _step_append_not_correct_input(message)

    N_index = _YES_TEXT.split(' ').index('{N}')
    description_id_index = _YES_TEXT.split(' ').index('{description_id}')

    N = text.split(' ')[N_index]
    description_id = text.split(' ')[description_id_index]
    try:
        N = int(N)
        description_id = uuid.UUID(description_id)
    except:
        return _step_append_not_correct_input(message)

    samples = list()
    for i in range(N):
        sample = Sample.make(
            description_id=description_id,
            user_id_create=user_id,
            user_id_owner=user_id,
            status=SampleStatus.init,
        )
        samples.append(sample)

    with Session(engine) as session:
        for sample in samples:
            session.add(sample)
            session.commit()
        for sample in samples:
            session.refresh(sample)
            session.expunge(sample)

    uuid_texts = [f'<code>{sample.id}</code>' for sample in samples]
    uuid_text = '\n'.join(uuid_texts)

    bot.send_message(
        message.chat.id,
        f"""Создано {N} экземпляров книг для <code>{description_id}</code> книги.
Всем им присвоен статус: <b>{SampleStatus.init}</b>.

У вас всего <u>{count_samples(user_id, SampleStatus.init)}</u> книг с этим статусом. 

Чтобы выгрузить наклейки, воспользуйтесь командой:
<code>
/pull_samples
</code>

UUID-ы добавленных экземпляров:
{uuid_text}

""",
        parse_mode='HTML',
        reply_markup=telebot.types.ReplyKeyboardRemove(),
    )
    return


@bot.message_handler(commands=["new_samples"])
def new_samples(message, res=False):
    command = message.text.strip()
    values = command.split(' ')

    if len(values) != len('/new_samples description_id --count N'.split(' ')):
        return _not_correct_format(message)

    try:
        description_id = uuid.UUID(values[1])
    except:
        return _not_correct_format(message)

    if values[2] != '--count':
        return _not_correct_format(message)

    try:
        N = int(values[3])
    except:
        return _not_correct_format(message)

    with Session(engine) as session:
        description = session.get(Description, description_id)
        if description is None:
            return _not_found_description_id(message, description_id)

        description.send_message_about(
            bot,
            message.chat.id,
        )

        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

        markup.add(telebot.types.KeyboardButton(_NO_TEXT))
        markup.add(telebot.types.KeyboardButton(_YES_TEXT.format(N=N, description_id=description_id)))

        message_next = bot.send_message(
            message.chat.id,
            f"""Вы желаете добавить <u>{N}</u> <b>новых</b> экземпляров книги к
        описанию книги <code>{description_id}</code>?""",
            reply_markup=markup,
            parse_mode='HTML',
        )
        bot.register_next_step_handler(message_next, _step_append)

