#!/bin/bash

wait_for_postgres() {
    until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
        echo "PostgresSQL is not available. Waiting..."
        sleep 2
    done
    echo "PostgresSQL started"
}

wait_for_postgres
echo "PostgreSQL is ready. Proceed with your script."

echo "Applying migrations..."
python manage.py migrate --noinput
pytest

python manage.py createsuperuser --no-input || echo "Superuser already exists or cannot be created"

echo "Starting Server..."
python manage.py runserver 0.0.0.0:8000