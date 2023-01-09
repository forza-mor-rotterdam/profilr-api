#!/usr/bin/env bash
set -u   # crash on missing env variables
set -e   # stop on any error
set -x

echo Collecting static files
python manage.py collectstatic --no-input

chmod -R 777 /static

# echo Apply migrations
# python manage.py migrate --noinput

echo Create superuser
python manage.py createsuperuser --noinput || true

echo Create cachetable
python manage.py createcachetable

exec uwsgi --ini /app/deploy/config.ini
