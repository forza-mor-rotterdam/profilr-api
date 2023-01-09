#!/usr/bin/env bash
set -u   # crash on missing env variables
set -e   # stop on any error
set -x

echo Collecting static files
python manage.py collectstatic --no-input

chmod -R 777 /static

echo Apply migrations
python manage.py migrate db zero
python manage.py migrate --noinput

echo Create superuser
python manage.py createsuperuser --noinput || true

echo Create cachetable
python manage.py createcachetable

exec python -m debugpy --listen 0.0.0.0:5678 ./manage.py runserver 0.0.0.0:8000
