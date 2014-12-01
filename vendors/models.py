#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from utils.models import Proto
from stdimage.models import StdImageField

class Vendor(Proto):
    
    image = StdImageField(
        upload_to="vendors", 
        verbose_name=u"Картинка",
        null=True,
        blank=True,
        variations={
            "thumbnail": (128, 128),
            "medium": (512, 512),
        } 
    )
    
    class Meta :
        verbose_name = u"Производитель"
