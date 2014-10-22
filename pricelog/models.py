#-*- coding: utf-8 -*-

from django.db import models
from utils.models import Proto

class Price(models.Model, Proto):

    class Meta :
        verbose_name = u"Прайс"
