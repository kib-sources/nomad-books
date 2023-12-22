# nomad-books
Книги кочевников. Online система offline обмена книгами




## Запуск (Local Dev)

### Postgres

Для удобства установите
```bash
sudo apt install postgresql-client postgresql-client-common
```



Выгрузите образ Postgres:
```bash
~$ docker pull postgres:16.1
```

Запустите Postgres.
Если запускаете в первый раз:
```bash
~$ export $(grep -v '^#' .env | xargs)
~$ docker run --name postgres -e POSTGRES_USER=$POSTGRES_USER -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD -e POSTGRES_DB=$POSTGRES_DB -p 5432:$POSTGRES_PORT -d postgres
```

Если запускаете **не** в первый раз:
```bash
~$ docker ps -a
CONTAINER ID   IMAGE      COMMAND                  CREATED          STATUS                      PORTS     NAMES
02215bd48d49   postgres   "docker-entrypoint.s…"   45 seconds ago   Exited (0) 33 seconds ago             postgres
~$ docker start 02215bd48d49
```
Где вместо `02215bd48d49` укажите `CONTAINER ID`, выданный через `docker ps -a`

Проверьте, что Postgres запущен:
```commandline
~$ psql postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@localhost:$POSTGRES_PORT/$POSTGRES_DB
...
nomad=# \q
```

### Prisma + прогрузка базы данных

Установка
```bash
~$ npm install prisma --save-dev
```

Если старая версия  `nodejs`, то:
```bash
~$ curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
~$ sudo apt install -y nodejs
~$ nodejs --version

```


Прогрузка БД
```bash
~$ source .../bin/activate
~(venv)$ export $(grep -v '^#' .env | xargs)
~(venv)$ prisma db pull
```



## Запуск (Release)


## Что делаем

Первый документ: [~/doc/first.md](doc/first.md)

User Case: [~/doc/uc.md](doc/uc.md)

Архитектура:
* [С1](doc/c1.md)