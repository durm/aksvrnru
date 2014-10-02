#-*- coding: utf-8 -*-

import sys
sys.path.insert(0, "/home/durm/envs/aksvrn/lib/python2.7/site-packages")

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aksvrnru.settings")

import locale
locale.setlocale(locale.LC_TIME,'en_US.utf8')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
