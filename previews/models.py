#-*- coding: utf-8 -*-

from django.db import models
from utils.models import Proto
from stdimage.models import StdImageField
from aksvrnru.utils import *

def get_filename():
    path = get_id()
    return u"previews/%s/%s" % (path[:3], path)

def get_filename_model(instance, filename):
    return get_filename()

class Preview(Proto):

    image = StdImageField(
        upload_to=get_filename_model, 
        verbose_name=u"Файл",
        variations={
            "large": (1024, 1024),
            "thumbnail": (128, 128),
            "medium": (512, 512),
        } 
    )
    
    class Meta :
        verbose_name = u"Превью"













    
