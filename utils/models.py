#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class Proto(models.Model):

    name = models.CharField(
        max_length=255, 
        verbose_name=u"Название"
    )

    desc = models.TextField(
        blank=True,
        null=True,
        verbose_name=u"Описание"
    )

    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=u"Дата создания"
    )

    created_by = models.ForeignKey(
        User, 
        related_name="+cr+", 
        blank=True, 
        null=True, 
        verbose_name=u"Создал"
    )

    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name=u"Дата изменения"
    )
    
    updated_by = models.ForeignKey(
        User, 
        related_name="+up+", 
        blank=True, 
        null=True, 
        verbose_name=u"Изменил"
    )

    def __unicode__(self):
        return "%s" % (self.name)

    class Meta:
        abstract = True
