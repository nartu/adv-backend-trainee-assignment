# Инструкция по запуску

## Docker-compose

1. Клонировать репозиторий `git clone https://github.com/nartu/adv-backend-trainee-assignment.git`

2. `docker-compose up -d`

3. Запустить тесты:
  Сначала зайти в контейнер:
  ```
  docker exec -it app bash
  ```
  Тест соединения с БД и наличия таблиц:
  ```
  cd tests
  pytest -v test_db.py
  ```
  Тест основных функций приложения и тестовые объявления:

  `pytest -v test_main.py`

  Чтобы нагенерить их ещё, можно запустить:

  `pytest -v -k test_ads_create_success test_main.py`

4. Автоматическая интерактивная документация от fastapi http://0.0.0.0:9000/docs

5. Если не нужно сохранять данные БД, закомментить строчки в файле `docker-compose.yml`:
  ```
  # - dbdata:/var/lib/postgresql/data
  ...
  # volumes:
  #   dbdata:
  ```


## Вручную

1. Клонировать репозиторий `git clone https://github.com/nartu/adv-backend-trainee-assignment.git`

2. Установить базу данных Postgresql (если нет)
`sudo apt install postgresql`

  Подробнее https://www.postgresqltutorial.com/install-postgresql-linux/

3. Задать пароль суперюзеру postgres
  ```
  sudo -i -u postgres
  psql
  \password postgres
  --exit
  \q
  ```

4. Сделать sh файлы исполняемыми
`chmod u+x db_init_manually.sh uvicorn_start.sh src/prestart.sh`

5. Создать новую БД и таблицы в ней
`./db_init_manually.sh.sh`

  ИЛИ вручную из консоли psql
  ```
  psql
  --create new db
  \i ./db_init/sql/0_db_create_by_default.sql
  --show all databases (must be advtest)
  \l
  --change current db
  \c advtest
  --create tables
  \i ./db_init/sql/1_db_schema.sql
  --show tables
  \dt
  --exit
  \q
  ```

6. Установить виртуальное окружение
`virtualenv anvtest_venv`
ИЛИ
`python3 -m venv anvtest_venv`

7. Зайти в виртуальное окружение
`source anvtest_venv/bin/activate`
(команда для выхода `deactivate`)

8. Установить необходимые пакеты
  ```
  ./src/prestart.sh
  ```
  ИЛИ
  ```
  pip install --upgrade pip
  pip install -r src/requirements.txt
  ```

9. В файле `src/settings.py` установить конфиг для psql `DB_CONNECT_CONFIG = 'db_localhost.ini'`

10. Запуск приложения
`./uvicorn_start.sh`

11. Запуск тестов и добавление тестовых объявлений (в test_main.py (base_url) хост и порт должен совпадать с тем что указано в uvicorn_start.sh).

  Тест соединения с БД и наличия таблиц:
  ```
  cd src/tests
  pytest -v test_db.py
  ```
  Тест основных функций приложения и тестовые объявления:

  `pytest -v test_main.py`

  Чтобы нагенерить их ещё, можно запустить:

  `pytest -v -k test_ads_create_success test_main.py`

12. Автоматическая интерактивная документация от fastapi http://0.0.0.0:9000/docs
