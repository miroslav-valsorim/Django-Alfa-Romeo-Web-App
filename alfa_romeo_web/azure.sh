
python manage.py makemigrations

sleep 20

python manage.py migrate

sleep 20

python manage.py collectstatic --noinput

sleep 20

gunicorn --bind=0.0.0.0 alfa_romeo_web.wsgi