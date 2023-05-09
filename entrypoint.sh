#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python news_app/manage.py makemigrations
python news_app/manage.py migrate
python news_app/manage.py runserver 0.0.0.0:8000

exec "$@"
