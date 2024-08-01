#!/bin/sh

# Enter the alfa_romeo_web directory or exit if it fails
cd alfa_romeo_web || { echo "Failed to enter alfa_romeo_web directory"; exit 1; }

# Install requirements
pip install -r requirements.txt

# Makemigrations cos the PayPal ipn
python manage.py makemigrations

# Migrate all tables
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput || { echo "Failed to collect static files"; exit 1; }

# Start the gunicorn server
gunicorn --bind=0.0.0.0 alfa_romeo_web.wsgi || { echo "Failed to start gunicorn"; exit 1; }
