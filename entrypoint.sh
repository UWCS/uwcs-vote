#!/bin/bash

./.venv/bin/python manage.py migrate

exec ./.venv/bin/gunicorn uwcsvote.wsgi -w 4 -b 0.0.0.0:8080