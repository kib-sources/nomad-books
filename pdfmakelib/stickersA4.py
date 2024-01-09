"""

Библиотечка по созданию наклеек в стиле A4

Create at 29.12.2023 17:10:59
~/pdfmakelib/stickersA4.py
"""

__author__ = 'pavelmstu'
__copyright__ = 'KIB, 2023'
__license__ = 'KIB'
__credits__ = [
    'pavelmstu',
]
__version__ = "20231229"
__status__ = 'Develop'

# __status__ = "Production"

from dataclasses import dataclass

from uuid import UUID

import os
import io

from typing import List

from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from reportlab.lib.units import mm, inch

from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# A4 = (210*mm,297*mm), x -- 0, y -- 1
from reportlab.lib.pagesizes import A4

from reportlab.graphics.barcode import qr

from models.sample import Sample

# Количество стикеров на одну страницу
# Пока параметр НЕЛЬЗЯ менять...
COUNT_BY_ONE_PAGE = 8

# ---------------------------------------------------------------------------------------------------------------------
# Settings
# данные параметры можно менять

# путь к *.ttf файлам
FONT_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'fonts',
)

ORGANIZATION_LOGO_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'pics',
    'kib_logo.png'
)

TELEGRAM_LOGO_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'pics',
    'telegram.png',
)

pdfmetrics.registerFont(TTFont('OpenGostTypeA', os.path.join(FONT_PATH, 'OpenGostTypeA-Regular.ttf')))

main_font = 'OpenGostTypeA'

# Граница листа A4 по верху, низу и по бокам.
border = 15*mm

# границы в рамках одной карточки по верху, низу и по обоим бокам.
card_border = 3*mm

# радиус закругления у прямоугольников карточек
radius_roundRect = 5*mm

# количество карточек по оси x и по оси y
count_by_x = 2
count_by_y = 4

x_full_title_offset = -5*mm
y_full_title_offset = -1*mm

qr_width = qr_height = 50*mm

# оффсет для QR кода, чтобы ниже разместить две строки:
# 1. description_id=66d883b2-9760-4d8d-843e-9c62bec80887
# 2. sample_id=89201402-9a96-4a56-8de8-aa6e663b1f5d
y_uuid_bottom_text_offset = 5*mm

# ---------------------------------------------------------------------------------------------------------------------

# При смене шрифта вычислять через test_check_max_full_title()
max_symbols_full_title = 46
draw_card_full_title_size = 10

# шрифт UUID-ов
draw_card_uuids_size = 13
height_text = 5 * mm

organization_telegram = '@kibinfo'
organization = os.getenv('ORGANIZATION', "KIB")

# МАКСИМАЛЬНОЕ общее количество карточек на один лист A4
max_count_cards = count_by_x * count_by_y

# x -- 0, y -- 1
# ширина и высота одной карточки
card_width = (A4[0] - border*2) // count_by_x
card_height = (A4[1] - border*2) // count_by_y

assert card_border * 2 + radius_roundRect * 2 < card_height
assert card_border * 2 + radius_roundRect * 2 < card_width

# стартовые точки
card_start_points = list()
for yi in range(count_by_y):
    # y координата идёт от нижнего левого угла, а мы хотим начинать с верхнего левого
    y = A4[1] - ((yi+1) * card_height) - border
    for xi in range(count_by_x):
        x = xi * card_width + border
        _start_points = (x, y)
        card_start_points.append(_start_points)
        continue

assert len(card_start_points) == max_count_cards


_PATH = os.path.dirname(os.path.abspath(__file__))
print(f"_PATH={_PATH}")


def test1():
    c = canvas.Canvas(os.path.join(_PATH, "hello.pdf"), pagesize=A4)
    c.drawString(10*mm, 10*mm, "Welcome to Reportlab!")
    c.save()


def draw_qr_code(
    c: canvas.Canvas,
    qr_code: qr.QrCodeWidget,
    index: int,
):
    b = qr_code.getBounds()
    w = b[2] - b[0]
    h = b[3] - b[1]

    d = Drawing(qr_width, qr_height, transform=[qr_width / w, 0, 0, qr_height / h, 0, 0])
    # d = Drawing(1, 1)
    d.add(qr_code)

    x, y = card_start_points[index]

    renderPDF.draw(d, c, x+radius_roundRect, y+radius_roundRect+y_uuid_bottom_text_offset)


def draw_uuids(
        c: canvas.Canvas,
        description_id: UUID,
        sample_id: UUID,
        index: int ,
):
    x, y = card_start_points[index]

    c.setFont(main_font, draw_card_full_title_size)

    c.drawString(
        x+card_border+radius_roundRect+x_full_title_offset,
        y+card_border+radius_roundRect-y_full_title_offset,
        f'{description_id}',
    )

    c.drawString(
        x + card_border + radius_roundRect + x_full_title_offset,
        y + card_border + radius_roundRect - y_full_title_offset-height_text,
        f'{sample_id}',
    )


def draw_logo(
        c: canvas.Canvas,
        index: int,
):

    with open(ORGANIZATION_LOGO_PATH, 'rb') as fr:
        bytes = fr.read()
        organization_image = ImageReader(io.BytesIO(bytes))

    x, y = card_start_points[index]

    logo_width = 27 * mm
    logo_height = 27 * mm

    c.drawImage(
        organization_image,
        x + card_width - logo_width - card_border*2,
        y + card_height - logo_height - card_border*2 - 3 * mm,
        width=logo_width, height=logo_height, mask='auto')

    '''
    with open(TELEGRAM_LOGO_PATH, 'rb') as fr:
        bytes = fr.read()
        telegram_image = ImageReader(io.BytesIO(bytes))

    telegram_logo_width = 7 * mm
    telegram_logo_height = 7 * mm

    c.drawImage(
        telegram_image,
        x + card_width - logo_width - card_border * 2 ,
        y + card_height - logo_height - card_border * 2 - 3 * mm - telegram_logo_height - 3 * mm,
        width=telegram_logo_width, height=telegram_logo_height,
        mask='auto',
    )
    # '''

    # --
    telegram_size_text = 15
    telegram_height_text = 7 * mm
    telegram_y_offset = 3 * mm
    # ---

    c.setFont(main_font, telegram_size_text)
    c.drawString(
        x + card_width - logo_width - card_border * 2,
        y + card_height - logo_height - card_border * 2 - telegram_y_offset - telegram_height_text,
        "Telegram:",
    )

    c.drawString(
        x + card_width - logo_width - card_border * 2,
        y + card_height - logo_height - card_border * 2 - telegram_y_offset - telegram_height_text * 2,
        organization_telegram,
    )


def draw_card(
        c: canvas.Canvas,
        index: int,
        *,
        full_title: str,
        description_id: UUID,
        sample_id: UUID,
):
    nomad_books_qr_protocol = 'v1'

    assert 0 <= index < len(card_start_points)

    x, y = card_start_points[index]

    c.roundRect(x, y, card_width-card_border, card_height-card_border, radius=radius_roundRect, stroke=1, fill=0)

    if len(full_title) <= max_symbols_full_title:
        _full_title = full_title
    else:
        _full_title = full_title[:max_symbols_full_title-1]+"..."

    # c.setFont("Hebrew", 14)
    c.setFont(main_font, draw_card_full_title_size)
    c.drawString(
        x+card_border+radius_roundRect+x_full_title_offset,
        y-card_border-radius_roundRect-y_full_title_offset+card_height,
        _full_title,
    )

    qr_code_string = f'nomad_books_qr_protocol={nomad_books_qr_protocol}||organization={organization}||description_id={description_id}||sample_id={sample_id}||full_title={full_title[:60]}'
    print(f"index={index}, full_title={full_title}, qr_code_string={qr_code_string}")
    qr_code = qr.QrCodeWidget(qr_code_string)

    draw_qr_code(c, qr_code, index=index)

    draw_uuids(c, description_id=description_id, sample_id=sample_id, index=index)

    draw_logo(c, index=index)


def test_check_max_full_title():
    """
    С помощью этой функции можно вычислить max_symbols_full_title
    """
    import uuid
    c = canvas.Canvas(os.path.join(_PATH, "test_check_max_full_title.pdf"), pagesize=A4)

    for index in range(max_count_cards):
        draw_card(
            c, index,
            full_title='Детская энциклопедия, Том 3, издание третье',
            # full_title="123456789 1113151719212325272931333537394143454749515355575961",
            # full_title="ЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩЩ",
            # full_title='Harry Potter',
            description_id=uuid.uuid4(),
            sample_id=uuid.uuid4(),
            # copy_right_text='Данная книга является собственностью АНО "Клуб Информационной Безопасности (9717099769, 1217700108504)'
        )

    c.save()


@dataclass
class CardInfo:
    full_title: str
    description_id: UUID
    sample_id: UUID


def make_A4_stickers(
    *,
    cards: List[CardInfo],
    pdf_file_path: str,
):
    # for sample in samples:
    #     if sample.status != SampleStatus.init:
    #         ...
    assert pdf_file_path.endswith('.pdf')

    c = None
    i = 0
    count_pages = None
    while True:
        cards_chunk = cards[i*COUNT_BY_ONE_PAGE:(i+1)*COUNT_BY_ONE_PAGE]
        if len(cards_chunk) == 0:
            break

        if c is None:
            c = canvas.Canvas(pdf_file_path, pagesize=A4)
            count_pages = 1
        else:
            # Close the current page and possibly start on a new page.
            c.showPage()
            c.setPageSize(A4)
            count_pages += 1

        for index, card in enumerate(cards_chunk):
            draw_card(
                c, index,
                full_title=card.full_title,
                description_id=card.description_id,
                sample_id=card.sample_id,
            )

        i += 1
        continue

    c.save()
    return count_pages


if __name__ == "__main__":
    # test1()
    test_check_max_full_title()