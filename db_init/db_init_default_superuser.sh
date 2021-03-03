#!/usr/bin/bash

psql -U postgres < /docker-entrypoint-initdb.d/sql/0_db_create_by_default.sql &&
psql -U postgres advtest < /docker-entrypoint-initdb.d/sql/1_db_schema.sql
