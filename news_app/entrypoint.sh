#!/bin/sh

echo "$POSTGRES_DB"


python manage.py makemigrations
python manage.py migrate

exec "$@"
