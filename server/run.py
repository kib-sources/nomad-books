"""
<nomad-books>
server/run.py
    create by pavelmstu in 16.10.2023
--------------------------------------------------------

server.run -- запускаемый файл

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
import uvicorn

from server.api import app

# --------------------------------------------------------------------------------------------------------------------
# ! не убирать импорты -- они подписывают необходимые функции GET и POST запросов
import server.api.auth  # !
# --------------------------------------------------------------------------------------------------------------------

from settings import  API_HOST, API_PORT, SSL_KEYFILE_PASSWORD


def main():
    assert SSL_KEYFILE_PASSWORD, "Переменная SSL_KEYFILE_PASSWORD не задана!"
    uvicorn.run(
        app,
        # host=PIPELINES_API_HOST,
        host=API_HOST,
        port=API_PORT,
        ssl_keyfile='certs/key.pem',
        ssl_certfile='certs/cert.pem',
        ssl_keyfile_password=SSL_KEYFILE_PASSWORD,
    )


# --------------------------------------------------------- 
if __name__ == "__main__":
    # run mode
    main()
    exit()
else:
    # import mode
    pass
