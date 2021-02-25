# Инструкция по запуску

## Вручную

1. Клонировать репозиторий git clone https://github.com/nartu/adv-backend-trainee-assignment.git

2. Установить базу данных Postgresql, если нет
`sudo apt install postgresql`
Подробнее https://www.postgresqltutorial.com/install-postgresql-linux/

3. Задать пароль суперюзеру postgres
`sudo -i -u postgres
psql`
`\password postgres
--exit
\q
`
4. Сделать sh файлы исполняемыми
`chmod u+x db_init.sh uvicorn_start.sh`

5. Создание новой БД и таблиц в ней
`./db_init.sh`
ИЛИ вручную из консоли psql
`psql`
`--create new db
\i ./db_create.psql
--show all databases (must be advtest)
\l
--change current db
\c advtest
--create tables
\i ./db+schema.sql
--show tables
\d
--exit
\q
`
6. Установить виртуальное окружение
`virtualenv anvtest_venv`
ИЛИ
`python3 -m venv anvtest_venv`

7. Зайти в виртуальное окружение
`source anvtest_venv/bin/activate`
(команда для выхода `deactivate`)

8. Установка необходимых пакетов
`pip install --upgrade pip`
`pip install -r requirements.txt`

9. Запуск приложения
`./uvicorn_start.sh`

10. Запуск тестов и добавление тестовых объявлений
Тест соединения с БД и наличия таблиц
`cd src/tests`
`pytest -v test_db.py`
Тест основных функций приложения и тестовые объявления
`pytest -v test_main.py`
Чтобы нагенерить их ещё, можно запустить
`pytest -v -k test_ads_create_success test_main.py`

11. Автоматическая интерактивная документация от fastapi http://0.0.0.0:8008/docs
(порт и хост указать в файле uvicorn_start.sh,
  так же следует указать другой адрес в test_main.py (base_url))
