"""
<nomad-books>
server/api/__init__.py
    create by pavelmstu in 16.10.2023
--------------------------------------------------------

Основной файл для импорта API приложения

>> from server.api import app
>> import api........... # !
>> import api........... # !
>> uvicorn.run(
        app,
        # host=PIPELINES_API_HOST,
        host=API_HOST,
        port=API_PORT,
        ssl_keyfile='certs/key.pem',
        ssl_certfile='certs/cert.pem',
        ssl_keyfile_password=SSL_KEYFILE_PASSWORD,
    )

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
__status__ = "Production"

import os

from typing import Annotated

from fastapi import Depends
from fastapi import FastAPI

from settings import API_HOST, API_PORT
from settings import ORGANIZATION

from functools import partial

from db.user import UserRole

app = FastAPI()


@app.get("/")
async def root():

    return {
        "message": f"API кочевой библиотеки. {ORGANIZATION}",
        "about": "Внутренняя API точка для доступа к продуктовой, технической и экспертной телеметрии",
        "version": __version__,
        "github": "",
        "docs": [
            f"https://{API_HOST}:{API_PORT}/docs",
            f"https://{API_HOST}:{API_PORT}/redoc",
        ],
        "contacts": [
            "https://t.me/lifestreamy",
            "https://t.me/pavelmstu",
        ]
    }


def _grants(func, grant: UserRole):
    # TODO разработать функцию-декоратор

    return func


# grants_mentor = partial(_grants, UserRole.mentor)
grants_leader = partial(_grants, UserRole.leader)
grants_admin = partial(_grants, UserRole.admin)
grants_maintainer = partial(_grants, UserRole.maintainer)
grants_owner = partial(_grants, UserRole.owner)


# TODO IAM добавить
'''
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        API_HOST,
        "172.24.5.250",
    ]
)
# '''



# https://fastapi.tiangolo.com/tutorial/dependencies/
async def user_parameters(
    user: str,
):
    return {

    }


UserParameters = Annotated[dict, Depends(user_parameters)]