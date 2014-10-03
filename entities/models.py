#-*- coding: utf-8 -*-

from django.db import models
import uuid

def file_upload_path(instance, filename):
    return u"entities/%s" % str(instance.id)

class Entity(models.Model):

    uuid = models.CharField(max_length=128, verbose_name=u"UUID")

    name = models.CharField(max_length=255, verbose_name=u"Название")
    desc = models.TextField(blank=True, null=True, verbose_name=u"Описание")

    file = models.FileField(upload_to=file_upload_path, verbose_name=u"Файл")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания")
    created_by = models.ForeignKey(User, related_name='+cr+', blank=True, null=True, verbose_name=u"Создал")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    updated_by = models.ForeignKey(User, related_name='+up+', blank=True, null=True, verbose_name=u"Изменил")
    
    def __unicode__(self):
        name = self.name if self.name else self.file.name
        return u"%s" % (name)

    class Meta :
        verbose_name = u"Файлы"
