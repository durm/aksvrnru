#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from utils.models import Proto

class Vendor(Proto):
    
    class Meta :
        verbose_name = u"Производитель"
