#!/bin/bash
set -e

postgres_ready() {
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(
        dbname="${POSTGRES_DB}",
        user="${POSTGRES_USER}",
        password="${POSTGRES_PASSWORD}",
        host="${DB_HOST}",
        port=5432
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

alembic upgrade heads

# Initialize database and start Flask app
exec python app.py