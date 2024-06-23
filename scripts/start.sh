#!/bin/bash


python manage.py migrate
pytest

echo "Starting Server..."
python manage.py runserver 0.0.0.0:8000