#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from utils.models import Proto

class Vendor(Proto):
    
    image = models.ImageField(
        upload_to=u"rubrics", 
        verbose_name=u"vendors",
        null=True, 
        blank=True
    )
    
    class Meta :
        verbose_name = u"Производитель"
