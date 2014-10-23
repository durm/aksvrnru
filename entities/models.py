#-*- coding: utf-8 -*-

from django.db import models
from django.core.files.base import ContentFile
from utils.models import Proto
import zipfile
from aksvrnru.utils import *

def get_filename():
    path = get_id()
    return u"entities/%s/%s" % (path[:3], path)

def get_filename_model(instance, filename):
    return get_filename()

class Entity(Proto):

    file = models.FileField(
        upload_to=get_filename_model, 
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
                content = ContentFile(zf.open(e).read())
                entity = Entity(
                    name=name, 
                    desc=desc 
                )
                entity.file.save(get_filename(), content, save=True)
                print(name)
            except Exception as e:
                print("Error: %s" % str(e))
        with zipfile.ZipFile(zp, "r") as zf :
            c = 0
            for e in zf.namelist() :
                if is_entity(e) :
                    c += 1
                    print "%s) " % str(c),
                    store(zf, e)

    class Meta :
        verbose_name = u"Файлы"

