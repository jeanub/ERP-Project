#!/bin/sh
set -e
until nc -z db 5432; do echo "Esperando postgres..."; sleep 1; done
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
