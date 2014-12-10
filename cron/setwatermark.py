#-*- coding: utf-8 -*-

import os, time, sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aksvrnru.settings")
from django.conf import settings
from aksvrnru.utils import add_watermark

fpath = sys.argv[1]
if os.path.exists(fpath):
    add_watermark(fpath, settings.WATERMARK)
