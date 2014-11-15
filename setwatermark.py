#-*- coding: utf-8 -*-

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aksvrnru.settings")
from django.conf import settings

from previews.models import Preview
from aksvrnru.utils import add_watermark

for preview in Preview.objects.all() :
    try:
        add_watermark(preview.image.medium.path, settings.WATERMARK)
        print "add", preview.id
    except Exception as e:
        print "-- error: %s" % str(e)

