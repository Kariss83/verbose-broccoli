#!/usr/bin/env bash
# exit on error
set -o errexit

sudo apt-get install libzbar0

pipenv install
pipenv install --dev

python manage.py collectstatic --no-input
python manage.py migrate