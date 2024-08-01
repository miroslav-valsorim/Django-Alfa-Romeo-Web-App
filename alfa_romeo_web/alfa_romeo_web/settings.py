import os
from pathlib import Path
import dj_database_url
from django.urls import reverse_lazy
from dotenv import load_dotenv

import cloudinary
import cloudinary.uploader
import cloudinary.api

# load .env file! It has to be in the same directory level as settings.py, asgi.py, urls.py, wsgi.py
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = os.environ.get('DEBUG', False) == 'True'

# ALLOWED_HOSTS = ['localhost', '127.0.0.1']
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(' ')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #  PayPal
    'paypal.standard.ipn',

    #  Django-REST
    'rest_framework',

    #  Our apps
    "alfa_romeo_web.accounts.apps.AccountsConfig",
    "alfa_romeo_web.main_page.apps.MainPageConfig",
    "alfa_romeo_web.museum.apps.MuseumConfig",
    "alfa_romeo_web.history.apps.HistoryConfig",
    "alfa_romeo_web.events.apps.EventsConfig",
    "alfa_romeo_web.news.apps.NewsConfig",
    "alfa_romeo_web.products.apps.ProductsConfig",
    "alfa_romeo_web.cart.apps.CartConfig",
    "alfa_romeo_web.checkout.apps.CheckoutConfig",
    "alfa_romeo_web.forum.apps.ForumConfig",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    #  Whitenoise to serve static in prod
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'alfa_romeo_web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'alfa_romeo_web.museum.context_processors.navbar_objects',
                'alfa_romeo_web.products.context_processors.navbar_product_objects',
            ],
        },
    },
]

WSGI_APPLICATION = 'alfa_romeo_web.wsgi.application'

# CONNECTION STRING FOR AZURE
# connection_string = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
# conn_str_params = {pair.split('=')[0]: pair.split('=')[1] for pair in connection_string.split(' ')}

# if facing and issue with test or prod db, remove the if, else statements
# and push the DB code one tab to the left
# problem could be the .env

if DEBUG:
    # Django default DB that I use wile DEBUG=True
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    # THE DB FOR DOCKER WHILE DEBUG=True
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql',
    #         'NAME': os.getenv("SQL_DATABASE", "hello_django_dev"),
    #         'USER': os.getenv("SQL_USER", "hello_django"),
    #         'PASSWORD': os.getenv("SQL_PASSWORD", "hello_django"),
    #         'HOST': os.getenv("SQL_HOST", "alfa-romeo-db"), # IMPORTRANT!! set db host to be the same as the docker-compose db service naming
    #         'PORT': os.getenv("SQL_PORT", "5432"),
    #     }
    # }
else:
    # THIS DB IS SET FOR DOCKER WHILE DEBUG=FALSE !!!!!
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql',
    #         'NAME': os.getenv("SQL_DATABASE", "hello_django_dev"),
    #         'USER': os.getenv("SQL_USER", "hello_django"),
    #         'PASSWORD': os.getenv("SQL_PASSWORD", "hello_django"),
    #         'HOST': os.getenv("SQL_HOST", "alfa-romeo-db"),# IMPORTRANT!! set db host to be the same as the docker-compose db service naming
    #         'PORT': os.getenv("SQL_PORT", "5432"),
    #     }
    # }

    # IM USING THIS FOR A PROD DB WHEN DEBUG=False !!!!
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv("DATABASE_URL", None),
            conn_max_age=600,
        )
    }

    # FOR AZURE DB SET UP
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql',
    #         'NAME': conn_str_params['dbname'],
    #         'HOST': conn_str_params['host'],
    #         'USER': conn_str_params['user'],
    #         'PASSWORD': conn_str_params['password'],
    #     }
    # }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

if DEBUG:
    # if DEBUG=True, no password validators
    AUTH_PASSWORD_VALIDATORS = ()
else:
    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

if DEBUG:
    STATIC_URL = 'static/'
    STATICFILES_DIRS = (
        BASE_DIR / 'staticfiles',
    )
else:
    # STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles')]
    STATIC_URL = 'static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Media files

if DEBUG:
    MEDIA_ROOT = BASE_DIR / 'mediafiles'
    MEDIA_URL = "/media/"
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
    MEDIA_URL = '/media/'

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
    secure=True,
)

CLOUDINARY_UPLOAD_OPTIONS = {

}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.AlfaRomeoUser'

LOGIN_REDIRECT_URL = reverse_lazy('main_page')

LOGIN_URL = reverse_lazy('login-user')

LOGOUT_REDIRECT_URL = reverse_lazy('main_page')

PAYPAL_RECEIVER_EMAIL = os.environ.get('PAYPAL_RECEIVER_EMAIL')
PAYPAL_TEST = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

# CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', '').split(' ')
# CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']]
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ.get('WEBSITE_HOSTNAME', 'localhost:8000')]