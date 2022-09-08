#!/bin/sh
set -e  # Configure shell so that if one command fails, it exits
coverage erase
coverage run manage.py test --verbosity 2
coverage report --ignore-errors --skip-covered -m
coverage html --ignore-errors --skip-covered