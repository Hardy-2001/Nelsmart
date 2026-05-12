#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --o-input

python manage.py migrate