#!/usr/bin/bash

psql -U postgres -h localhost < db_create.sql &&
psql -U postgres -h localhost advtest < db_schema.sql
