#-*- coding: utf-8 -*-

"""
Django settings for aksvrnru project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=18m%uc2k%c$0=f_#k^2vjm@se9e%lo9i=d@!a^v_n^qdkyj6o'

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (
    BASE_DIR + '/templates/'
)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'products',
    'kombu.transport.django',
    'djcelery',
)

CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
CELERY_CONCURRENCY = 2
BROKER_URL = 'django://'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'aksvrnru.urls'

WSGI_APPLICATION = 'aksvrnru.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases


MEDIA_URL = "/media/"

if os.path.exists(os.path.expanduser("~/aks_db.conf")):
    MEDIA_ROOT = os.path.expanduser("~/media/aksvrnru")
    dbconf = open(os.path.expanduser("~/aks_db.conf"), "r")
    DEBUG = True
else:
    MEDIA_ROOT = os.path.expanduser("/home/aksdjang/media/aksvrnru")
    dbconf = open(os.path.expanduser("/home/aksdjang/aks_db.conf"), "r")
    DEBUG = False


default_engine = eval(dbconf.read().strip())
dbconf.close()

STATIC_ROOT = os.path.join(BASE_DIR, "static")
WATER_MARK = os.path.join(STATIC_ROOT, "watermark.png")

DATABASES = {
    'default': default_engine
}

THREADED = False

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
