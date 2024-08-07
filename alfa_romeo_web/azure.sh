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
