"""
Команда /pull_samples

Create at 29.12.2023 16:19:28
~/tbot/pull_samples.py
"""

__author__ = 'pavelmstu'
__copyright__ = 'KIB, 2023'
__license__ = 'KIB'
__credits__ = [
    'pavelmstu',
]
__version__ = "20240109"
__status__ = "Production"

import datetime
import os.path
import tempfile

import telebot

from tbot import bot

from typing import List

from sqlalchemy import select, and_, or_, update

from sqlalchemy.orm import Session

from models import engine
from models.sample import Sample, SampleStatus
from models.description import Description

from tbot.common import get_samples

from tbot.errors import NomadDataExistsError

from pdfmakelib.stickersA4 import make_A4_stickers, CardInfo


_NO_TEXT = 'Отмена'
_YES_TEXT = 'Выгрузить'


def samples2card_info(samples: List[Sample]) -> List[CardInfo]:
    cards = list()

    with Session(engine) as session:
        for sample in samples:
            description = session.query(Description).filter_by(id=sample.description_id).one_or_none()
            if not description:
                raise NomadDataExistsError(f"Нет description_id={sample.description_id} для sample_id={sample.id}")

            card = CardInfo(
                full_title=description.full_title(),
                description_id=sample.description_id,
                sample_id=sample.id,
            )

            cards.append(card)

    return cards


def _step_append_not_correct_input(message):
    _ = bot.send_message(
        message.chat.id,
        f'''Ошибка ввода\\. 
Нужно ввести либо `{_NO_TEXT}`\\, либо `{_YES_TEXT}`''',
        parse_mode='MarkdownV2',
        reply_markup=telebot.types.ReplyKeyboardRemove(),
    )
    return


def _step_pull_error_input(message):

    bot.send_message(
        message.chat.id,
        f"""Ошибка ввода. Допустимые значения: <code>{_YES_TEXT}</code> и <code>{_NO_TEXT}</code>. Отмена.
""",
        reply_markup=telebot.types.ReplyKeyboardRemove(),
        parse_mode='HTML',
    )


def _step_pull(message):
    # "Отмена"
    # "Выгрузить"
    text = message.text
    user_id = message.from_user.id

    if text not in [_NO_TEXT, _YES_TEXT]:
        return _step_pull_error_input(message)

    if text == _NO_TEXT:
        bot.send_message(
            message.chat.id,
            f"""Отмена.""",
            reply_markup=telebot.types.ReplyKeyboardRemove(),
            parse_mode='HTML',
        )
        return

    assert text == _YES_TEXT

    samples = get_samples(user_id_owner=user_id, status=SampleStatus.init)

    try:
        cards = samples2card_info(samples)
    except NomadDataExistsError as e:
        bot.send_message(
            message.chat.id,
            getattr(e, 'message', repr(e)),
            reply_markup=telebot.types.ReplyKeyboardRemove(),
            parse_mode='HTML',
        )
        return

    bot.send_message(
        message.chat.id,
        f"""Выгрузка... \n(Подождите 1-2 минуты)""",
        reply_markup=telebot.types.ReplyKeyboardRemove(),
        parse_mode='HTML',
    )

    with tempfile.TemporaryDirectory() as tmpdirname:

        filename = f'stickers.{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        pdf_file_path = os.path.join(tmpdirname, filename)

        count_pages = make_A4_stickers(
            cards=cards,
            pdf_file_path=pdf_file_path,
        )

        # TODO сделать проверку:
        #  В настоящее время боты могут отправлять файлы любого типа размером до 50 МБ
        #  Однако для этого нужно более 6144 наклеек... Скорее всего этого не будет.
        pass

        with open(pdf_file_path, 'rb') as fr:
            message = bot.send_document(
                message.from_user.id,
                fr,
                caption=filename,
                reply_markup=telebot.types.ReplyKeyboardRemove(),
                timeout=600,
            )
            file_id = message.document.file_id

        bot.send_message(
            message.chat.id,
            f"""☝️Стикеры c <b>{len(cards)}</b> наклейками на {count_pages} страницах A4\n(file_id={file_id})""",
            reply_markup=telebot.types.ReplyKeyboardRemove(),
            parse_mode='HTML',
        )

    new_status = SampleStatus.pulled.value
    with Session(engine) as session:
        uuids = [card.sample_id for card in cards]
        stmt = update(Sample).where(Sample.id.in_(uuids)).values(status=new_status)
        session.execute(stmt)
        session.commit()

    bot.send_message(
        message.chat.id,
        f"""Статус поменян на <b>{new_status}</b>.""",
        reply_markup=telebot.types.ReplyKeyboardRemove(),
        parse_mode='HTML',
    )

    return


@bot.message_handler(commands=["pull_samples"])
def pull_samples(message, res=False):

    user_id = message.from_user.id

    samples = get_samples(user_id_owner=user_id, status=SampleStatus.init)

    if len(samples) == 0:
        _ = bot.send_message(
            message.chat.id,
            f"""У вас все <b>созданные вами</b> экземпляры книг со статусом <b>{SampleStatus.init.value}</b>
выгружены.

Отмена.
""",
            parse_mode='HTML',
            reply_markup=telebot.types.ReplyKeyboardRemove(),
        )
        return

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(telebot.types.KeyboardButton(_NO_TEXT))
    markup.add(telebot.types.KeyboardButton(_YES_TEXT))

    message_next = bot.send_message(
        message.chat.id,
        f"""Вы желаете выгрузить в A4 наклейки  <b>{len(samples)}</b> экземпляров книг 
и поменять их статус с <b>{SampleStatus.init.value}</b> на <b>{SampleStatus.pulled.value}</b> ?""",
        reply_markup=markup,
        parse_mode='HTML',
    )
    bot.register_next_step_handler(message_next, _step_pull)


