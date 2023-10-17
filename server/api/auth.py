"""
<nomad-books>
server/api/auth.py
    create by pavelmstu in 16.10.2023
--------------------------------------------------------

server.api.auth -- файл аутентификации данных

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
__status__ = "Development"

# __status__ = "Production"

import os

from typing import Annotated

from fastapi import Depends
from server.api import app



from db.application import ApplicationStatus

from fastapi.responses import JSONResponse


async def application_params(
    application_uuid: str,
    request_datetime: str,
):
    return {
        "application_uuid": application_uuid,
        "request_datetime": request_datetime,
    }

ApplicationParams = Annotated[dict, Depends(application_params)]

Signature = str


def check_sign(*args, sign, rsa_pub):
    message = '#'.join(str(a) for a in args)

    raise NotImplementedError()

    hash1 = ...
    hash2 = ...

    if hash1 == hash2:
        return True
    else:
        return False


@app.post("/auth/init")
def auth_init(
    application_params: ApplicationParams,
    rsa_pub: str,
    tg_name: str,
):
    """
    Инициализация нового приложения
    :param application_params:
    :param rsa_pub: публичный ключ RSA
    :param tg_name:
    :return:
    """
    application_uuid = application_params['application_uuid']
    request_datetime = application_params['request_datetime']

    # проверка что request_datetime в формате ISO
    # проверка request_datetime с точностью до +\- 5 минут
    pass

    # Проверка что application_uuid отсуствует в БД или присутствует и rsa_pub совпадают.
    pass

    # Проверка корректности rsa_pub
    pass

    # Проварка что tg_name есть в базе
    pass

    status = ApplicationStatus.not_authorized
    # Запись application_uuid со статусом `not_authorized'
    pass

    # Генерирование pin кода
    pin = "12345"

    # Запис pin кода во временное хранилище
    pass

    # Отправка pin кода чат боту, чтобы тот выслал пользователю код
    pass

    return JSONResponse(
        {
            "status": "ok",
            "error": None,
            "func": auth_init.__name__,
            "application_uuid": application_uuid,
            "application_status": str(status),
        },
        status_code=200,
    )


@app.post("/auth/pin")
def auth_pin(
    application_params: ApplicationParams,
    pin: str,
    sign: Signature,
):
    """

    :param application_params:
    :param pin:
    :param sign:
    :return:
    """
    application_uuid = application_params['application_uuid']
    request_datetime = application_params['request_datetime']

    # проверка что request_datetime в формате ISO
    # проверка request_datetime с точностью до +\- 5 минут
    pass

    # Проверка что application_uuid есть в БД, статус not_authorized и rsa_pub совпадают
    pass

    # выгрузка rsa_pub по application_uuid
    rsa_pub = ...

    if not check_sign(application_uuid, request_datetime, pin, sign=sign, rsa_pub=rsa_pub):
        # подпись не сходится
        return JSONResponse(
            {
                "status": "error",
                "error": "Signature is not correct",
                "func": auth_pin.__name__,
                "application_uuid": application_uuid,
            },
            status_code=401,
        )

    else:

        status = ApplicationStatus.authorized

        # меняем статус
        ...
        ...

        return JSONResponse(
            {
                "status": "ok",
                "error": None,
                "func": auth_pin.__name__,
                "application_uuid": application_uuid,
                "application_status": str(status),
            },
            status_code=200,
        )


@app.post("/auth/check")
def auth_check(
    application_params: ApplicationParams,
    sign: Signature,
):
    """
    Проверяет корректность аутентификации
    :param application_params:
    :param sign:
    :return:
    """
    application_uuid = application_params['application_uuid']
    request_datetime = application_params['request_datetime']


    # выгрузить статус
    status = ...

    # выгрузить rsa_pub
    rsa_pub = ...

    if not check_sign(application_uuid, request_datetime, sign=sign, rsa_pub=rsa_pub):
        # подпись не сходится
        return JSONResponse(
            {
                "status": "error",
                "error": "Signature is not correct",
                "func": auth_check.__name__,
                "application_uuid": application_uuid,
            },
            status_code=401,
        )
    else:
        # подпись не сходится
        return JSONResponse(
            {
                "status": "ok",
                "error": None,
                "func": auth_check.__name__,
                "application_status": status,
                "application_uuid": application_uuid,
            },
            status_code=401,
        )



