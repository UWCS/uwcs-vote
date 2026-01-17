#!/bin/bash

./.venv/bin/python manage.py migrate

./.venv/bin/python manage.py runscheduler &

exec ./.venv/bin/gunicorn uwcsvote.wsgi -w 4 -b 0.0.0.0:8080