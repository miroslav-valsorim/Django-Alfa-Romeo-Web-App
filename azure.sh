cd alfa_romeo_web || exit

python manage.py collectstatic --noinput

gunicorn --bind=0.0.0.0 alfa_romeo_web.wsgi