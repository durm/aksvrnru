#-*- coding: utf-8 -*-

import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = "=18m%uc2k%c$0=f_#k^2vjm@se9e%lo9i=d@!a^v_n^qdkyj6o"

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ["aks.djangohost.name", "aksvrn.ru"]

DOMAIN_ = "http://aks.djangohost.name/"

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "previews",
    "products",
    "markdown_deux",
    "pages",
    "userprofiles",
    "entities",
    "vendors",
    "rubrics",
    "utils",
    "pricelog",
    "stdimage",
)

MIDDLEWARE_CLASSES = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

ROOT_URLCONF = "aksvrnru.urls"

WSGI_APPLICATION = "aksvrnru.wsgi.application"

MEDIA_URL = "/media/"

if os.path.exists("/home/aksvrnru") :
    sys.path.append("/home/aksvrnru/config")
else:
    sys.path.append("..")
    
import aksconf

MEDIA_ROOT = aksconf.MEDIA_ROOT
DEBUG = aksconf.DEBUG
default_engine = aksconf.default_engine

STATIC_ROOT = os.path.join(BASE_DIR, "static")
WATER_MARK = os.path.join(STATIC_ROOT, "watermark.png")

DATABASES = {
    "default": default_engine,
}

THREADED = False

LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

STATICFILES_DIRS = (
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.csrf",
)

EMAIL_HOST = "smtp.yandex.ru"
EMAIL_HOST_PASSWORD = "infopass"
EMAIL_HOST_USER = "info@alexkorotkov.ru"
EMAIL_PORT = 25
EMAIL_USE_TLS = True

#NOTES_EMAIL = "aksesavto@yandex.ru"
NOTES_EMAIL_FROM = "durm.icecoffee@gmail.com"
NOTES_EMAIL_TO = "durm.icecoffee@gmail.com"

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  "templates"),
)
