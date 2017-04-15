"""
Django settings for earDetectionWebApp project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from kombu import Exchange, Queue
from sys import platform

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j@fw^tl-_@s5@2ii6s4!^5qz^jz@#%d*h#$=75npa&1ebv1=p%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['147.175.106.116','localhost','127.0.0.1']


SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'


# Application definition

INSTALLED_APPS = [
    'django_celery_results',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'earTrainer',
    'earDetector',
    'bootstrap3',
    'jquery',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    'PAGINATE_BY': 10
}

ROOT_URLCONF = 'earDetectionWebApp.urls'

FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler"
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'earDetectionWebApp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
properties = None
from earTrainer.main.utils import PropertyUtils
__prop = PropertyUtils()
# check if in docker
if os.path.exists('/.dockerenv'):
    properties = __prop.get_all('docker')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_ENV_DB', 'postgres'),
            'USER': os.environ.get('DB_ENV_POSTGRES_USER', 'postgres'),
            'PASSWORD': os.environ.get('DB_ENV_POSTGRES_PASSWORD', 'postgres'),
            'HOST': os.environ.get('DB_PORT_5432_TCP_ADDR', 'db'),
            'PORT': os.environ.get('DB_PORT_5432_TCP_PORT', '5432'),
        },
    }
else:

    if platform == 'linux':
        properties = __prop.get_all('linux')
    else:
        properties = __prop.get_all('main')

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'sqlite.db'),
        },
    }


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Bratislava'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_REDIRECT_URL = '/earTrainer/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# STATICFILES_DIRS = ( os.path.join(BASE_DIR, "static/"),
#                      os.path.join(STATIC_ROOT, 'css/'),
#                      os.path.join(STATIC_ROOT, 'javascript/'),
#                      os.path.join(STATIC_ROOT, 'images/')
#                     )

# For storing images loaded by users
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
MEDIA_URL = 'media/'

FILE_UPLOAD_TEMP_DIR = os.path.join(BASE_DIR,"media")


# Redis
REDIS_PORT = 6379
REDIS_DB = 0
#REDIS_HOST = 'devpassword@redis'
REDIS_HOST = os.environ.get('REDIS_PORT_6379_TCP_ADDR', 'redis')

RABBIT_HOSTNAME = os.environ.get('RABBIT_PORT_5672_TCP', 'rabbit')
if RABBIT_HOSTNAME.startswith('tcp://'):
    RABBIT_HOSTNAME = RABBIT_HOSTNAME.split('//')[1]

##### CELERY STUFF   ########
BROKER_URL = os.environ.get('BROKER_URL', '')

if not BROKER_URL:
    BROKER_URL = 'amqp://{user}:{password}@{hostname}/{vhost}/'.format(
        user=os.environ.get('RABBIT_ENV_USER', 'admin'),
        password=os.environ.get('RABBIT_ENV_RABBITMQ_PASS', 'mypass'),
        hostname=RABBIT_HOSTNAME,
        vhost=os.environ.get('RABBIT_ENV_VHOST', ''))

# We don't want to have dead connections stored on rabbitmq, so we have to negotiate using heartbeats
BROKER_HEARTBEAT = '?heartbeat=30'
if not BROKER_URL.endswith(BROKER_HEARTBEAT):
    BROKER_URL += BROKER_HEARTBEAT

#BROKER_POOL_LIMIT = 1
#BROKER_CONNECTION_TIMEOUT = 10

# configure queues, currently we have only one
CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
)

# Sensible settings for celery
CELERY_ALWAYS_EAGER = False
CELERY_ACKS_LATE = True
CELERY_TASK_PUBLISH_RETRY = True
CELERY_DISABLE_RATE_LIMITS = False

CELERY_IGNORE_RESULT = False
CELERY_SEND_TASK_ERROR_EMAILS = False
CELERY_TASK_RESULT_EXPIRES = 600

# Set redis as celery result backend

CELERY_RESULT_BACKEND = 'redis://%s:%d/%d' % (REDIS_HOST, REDIS_PORT, REDIS_DB)
#CELERY_RESULT_BACKEND = 'django-db'
CELERY_REDIS_MAX_CONNECTIONS = 10
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Bratislava'

CELERYD_HIJACK_ROOT_LOGGER = False
CELERYD_PREFETCH_MULTIPLIER = 1
CELERYD_MAX_TASKS_PER_CHILD = 1000