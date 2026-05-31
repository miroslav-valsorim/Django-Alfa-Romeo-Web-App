# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

COPY entrypoint.sh .
RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Collect static files at build time so they are baked into the image.
#
# WHY at build time: avoids running collectstatic on every pod restart and
# removes the need for a separate init container that caused permission issues.
#
# WHY these env vars are safe (they do NOT affect the running container):
#   - Variables set with RUN VAR=value only exist for this single build step.
#     They are NOT the same as ENV instructions and are NOT written into the
#     image environment. At runtime, Kubernetes injects the real values from
#     ConfigMap and Secret, completely replacing these.
#
#   SECRET_KEY=dummy-build-key
#     Django requires a non-empty SECRET_KEY to load settings. Any string works
#     here because collectstatic never uses it.
#
#   DATABASE_ENGINE=django.db.backends.sqlite3
#     Prevents settings.py from trying to configure a PostgreSQL connection
#     (which would fail since there is no DB during docker build).
#     collectstatic does not connect to the database at all, but settings.py
#     still needs a valid-looking DB config to load without errors.
#
#   DEBUG=False
#     Activates STATIC_ROOT and CompressedStaticFilesStorage in settings.py,
#     which is required for collectstatic to know where to write files and to
#     produce the .gz/.br compressed versions that Whitenoise serves in production.
#     With DEBUG=True, STATIC_ROOT is not defined and collectstatic would fail.
RUN SECRET_KEY=dummy-build-key \
    DATABASE_ENGINE=django.db.backends.sqlite3 \
    DEBUG=False \
    python manage.py collectstatic --noinput

ENTRYPOINT ["/app/entrypoint.sh"]

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
