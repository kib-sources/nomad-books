# pdfmakelib

Библиотечка по созданию PDF файла для наклеек.

Основная функция -- `make_A4_stickers`

Пример использования + выслать PDF чат ботом:

```python
count_pages = make_A4_stickers(
    cards=cards,
    pdf_file_path=pdf_file_path,
)

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
    f"""☝️Стикеры c <b>{len(cards)}</b> наклейками на {count_pages} страницах A4<br>(file_id={file_id})""",
    reply_markup=telebot.types.ReplyKeyboardRemove(),
    parse_mode='HTML',
)
```