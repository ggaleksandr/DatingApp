#!/bin/bash

set -x -e

# Replace djangouser, SUPERUSER_PASSWORD and django with your own values
# Don't forget to change them in .env file too!

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER djangouser WITH PASSWORD 'b16a780794acd81cf162724ea875d7d9e2c40e1bf64847ca66c80516e2afc671';
    CREATE DATABASE django;
    GRANT ALL PRIVILEGES ON DATABASE django TO djangouser;
    ALTER DATABASE django OWNER TO djangouser;
EOSQL

psql -U djangouser -d django < /var/lib/postgresql/dump/sql_backup_data.sql