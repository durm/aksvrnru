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

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'products'
)

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

default_engine = None

MEDIA_ROOT = os.path.expanduser("~/media/aksvrnru")
MEDIA_URL = os.path.expanduser("/media/")

try:
    dbconf = open(os.path.expanduser("~/aks_db.conf"), "r")
    default_engine = eval(dbconf.read().strip())
    STATIC_ROOT = os.path.expanduser("~/static/aksvrnru")
except:
    dbconf = open(os.path.expanduser("/home/aksdjang/aks_db.conf"), "r")
    default_engine = eval(dbconf.read().strip())

    MEDIA_ROOT = "/home/aksdjang/media/aksvrnru"
    STATIC_ROOT = "/home/aksdjang/static/aksvrnru"

DATABASES = {
    'default': default_engine
}

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
