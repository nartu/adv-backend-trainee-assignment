##!/usr/bin/python

import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="testbd",
    user="postgres",
    password="777"
)

print('PostgreSQL database version:')

# create a cursor
cur = conn.cursor()

cur.execute('SELECT version()')

# display the PostgreSQL database server version
db_version = cur.fetchone()
print(db_version)

conn.commit()
conn.close()
