#-*- coding: utf-8 -*-

from django.db import models
from utils.models import Proto
from stdimage.models import StdImageField
from aksvrnru.utils import *
from django.core.files.base import ContentFile
import zipfile
import traceback

def get_filename():
    path = get_id()
    return u"previews/%s/%s.jpg" % (path[:3], path)

def get_filename_model(instance, filename):
    return get_filename() 

class Preview(Proto):

    image = StdImageField(
        upload_to=get_filename_model, 
        verbose_name=u"Файл",
        variations={
            "thumbnail": (128, 128),
            "medium": (512, 512),
        } 
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
                try:
                    ne = e.decode('utf-8').encode('utf-8')
                except:
                    ne = e.decode('cp866').encode('utf-8')
                desc = ne
                name = get_name(ne)
                content = ContentFile(zf.open(e).read())
                entity = Preview(
                    name=name, 
                    desc=desc 
                )
                entity.image.save(get_filename(), content, save=True)
                #print(name)
            except Exception as e:
                #print("Error: %s" % str(e))
                traceback.print_exc()
        with zipfile.ZipFile(zp, "r") as zf :
            c = 0
            for e in zf.namelist() :
                if is_entity(e) :
                    c += 1
                    #print "%s) " % str(c),
                    store(zf, e)
    
    class Meta :
        verbose_name = u"Превью"
