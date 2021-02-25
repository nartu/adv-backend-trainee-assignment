import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
# print(sys.path)

import pytest
from db import Db

@pytest.fixture(scope="module")
def db_init():
    db = Db()
    print("Connect")
    yield db
    db.close()
    print("Disconnect")

def test_connection(db_init):
    assert db_init

def test_execute_one(db_init):
    db_res1 = db_init.execute_one('SELECT version()')
    db_res2 = db_init.execute_one('SHOW config_file')
    assert len(db_res1) > 0
    assert len(db_res2) > 0

def test_execute(db_init):
    # show tables
    sql = '''
    SELECT * FROM pg_catalog.pg_tables;
    '''
    db_res = db_init.execute(sql)
    assert db_res
    assert type(db_res) is dict
    assert len(db_res.get('psql_answer')) > 0

def test_tables_exist(db_init):
    # test tables was created ads_main, ads_photo
    sql = '''
    SELECT tablename
	FROM pg_catalog.pg_tables
	WHERE schemaname != 'pg_catalog' AND
	schemaname != 'information_schema';
    '''
    db_res = db_init.execute(sql)

    raw = db_res.get('psql_answer')
    assert len(raw) > 0

    tables = [item[0] for item in raw]
    tables_control = ['ads_main','ads_photo']

    assert tables == tables_control

def test_tables_schema(db_init):
    # must be columns
    # ads_main: id, name, description, price, created_at
    # ads_photo: id, main_id, photo_url
    sql = '''
    SELECT
       table_name,
       column_name,
       data_type
    FROM
       information_schema.columns
    WHERE
       table_name = 'ads_main'
       OR
       table_name = 'ads_photo';
    '''
    db_res = db_init.execute(sql)

    raw = db_res.get('psql_answer')
    assert len(raw) > 0

    tables_ads_main = [item[1] for item in raw if item[0] == "ads_main"]
    tables_ads_photo = [item[1] for item in raw if item[0] == "ads_photo"]
    tables_control_ads_main  = [i.strip() for i in \
        "id, name, description, price, created_at".split(',')]
    tables_control_ads_photo  = [i.strip() for i in \
        "id, main_id, photo_url".split(',')]

    assert tables_ads_main == tables_control_ads_main
    assert tables_ads_photo == tables_control_ads_photo
