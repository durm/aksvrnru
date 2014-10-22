#-*- coding: utf-8 -*-

from django.db import models
from django.core.files.base import ContentFile
from utils.models import Proto
import zipfile
from aksvrnru.utils import *

def get_filename(instance, filename):
    return u"entities/%s" % get_id()

class Entity(Proto):

    file = models.FileField(
        upload_to=get_filename, 
        null=False, 
        verbose_name=u"Файл"
    )

    @staticmethod
    def uploadFromZip(zp):
        def is_entity(e):
            return e.endswith(".jpg")
        def u(e):
            return e
        def get_name(e):
            return e.split("/")[-1][:-4]
        def store(zf, e): 
            try:
                desc = e
                name = get_name(e)
                entity = Entity(
                    name=name, 
                    desc=desc, 
                    file=ContentFile(zf.open(e).read())
                )
                entity.save()
                print(name)
            except Exception as e:
                print("Error: %s" % str(e))
        with zipfile.ZipFile(zp, "r") as zf :
            for e in zf.namelist() :
                if is_entity(e) :
                    store(zf, e)

    class Meta :
        verbose_name = u"Файлы"

