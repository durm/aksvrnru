#-*- coding: utf-8 -*-

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aksvrnru.settings")

os.environ['LANG']='ru_RU.UTF-8'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
