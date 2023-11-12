#!/bin/sh

python manage.py collectstatic --no-input --settings=config.production

python manage.py migrate --settings=config.production

python manage.py runserver 0.0.0.0:8000 --settings=config.production