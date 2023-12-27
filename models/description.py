"""
class Descriptions(BaseModel)

Create at 26.12.2023 15:42:49
~/models/description.py
"""

__author__ = 'pavelmstu'
__copyright__ = 'KIB, 2023'
__license__ = 'KIB'
__credits__ = [
    'pavelmstu',
]
__version__ = "20231226"
__status__ = 'Develop'

# __status__ = "Production"


# from sqlalchemy.orm import mapped_column
from sqlalchemy import Column
from sqlalchemy import Unicode, UnicodeText, SmallInteger, Integer, UUID, DateTime, LargeBinary, ARRAY, Boolean

import telebot

from models.base import BaseModel, new_id


GENRE_MAGAZINE = "журнал"

ProposedGenreList = [
    "учебник",
    "методичка",
    GENRE_MAGAZINE,  # "журнал",
    "справочник",
    "худ.лит.",
]


# TODO проблемы будут с многопоточностью
#   переписать на Redis
_CHAT_ID_DESCRIPTION = dict()


class Description(BaseModel):
    __tablename__ = "description"
    __table_args__ = {
        'comment': 'Описание различных книг и журналов (Экземпляры лежат в Samples таблице)'
    }
    # id, create_at, update_at, comment,

    title = Column(Unicode, nullable=False, comment="Заголовок книги или журнала (включая номер)")
    year = Column(SmallInteger, nullable=False, comment="Год издания")

    about = Column(UnicodeText, default=None, comment="Описание книги/журнала")

    authors = Column(ARRAY(Unicode), default=list, comment="Авторы книги/журнала")

    number = Column(SmallInteger, default=None, comment="номер (для журнала)")

    tags = Column(ARRAY(Unicode), default=list, comment="Теги")

    genre = Column(Unicode, default=None, comment=f"Жанр. Рекомендуемые: {', '.join(ProposedGenreList)}.")

    # main_foto: Optional[File]

    # foto_list: List[File] = Field(default_factory=list)

    enabled = Column(Boolean, default=False, comment="Если False, то книга ещё недоступна")

    def full_title(self):
        if self.number:
            return f"{self.title}, {self.number}"
        else:
            return self.title

    def completion(self, bot, m):
        global _CHAT_ID_DESCRIPTION
        _CHAT_ID_DESCRIPTION[m.chat_id] = self

    def telebot_edit_keyboard(self, bot, chat_id):
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

        button_about = telebot.types.KeyboardButton(text="about (описание книги)")
        keyboard.add(button_about)

        button_genre = telebot.types.KeyboardButton(text="genre (жанр)")
        button_authors = telebot.types.KeyboardButton(text="authors (авторы)")
        button_tags = telebot.types.KeyboardButton(text="tags")
        keyboard.add(button_genre, button_authors, button_tags)

        bot.send_message(
            chat_id,
            'Добавить\редактировать поля:',
            parse_mode='MarkdownV2',
            reply_markup=keyboard
        )




