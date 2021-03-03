#!/usr/bin/bash

psql -U postgres -h localhost < db_init/sql/0_db_create_by_default.sql &&
psql -U postgres -h localhost advtest < db_init/sql/1_db_schema.sql
