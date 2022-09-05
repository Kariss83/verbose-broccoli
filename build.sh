#!/usr/bin/env bash
# exit on error
set -o errexit

sudo apt update
sudo apt upgrade -y
pipenv install

python manage.py collectstatic --no-input
python manage.py migrate