#-*- coding: utf-8 -*-

from django.db import models
from datetime import date
from utils.models import Proto

class Page(Proto):
    
    title = models.CharField(
        max_length=255, 
        verbose_name=u"Краткое название"
    )

    content = models.TextField(
        verbose_name=u"Содержание"
    )

    parent = models.ForeignKey(
        "self", 
        blank=True, 
        null=True, 
        verbose_name=u"Родительская страница"
    )

    def has_children(self):
        return len(Page.objects.filter(parent=self)[:1]) == 1 #lazy

    def children(self):
        return Page.objects.filter(parent=self)

    class Meta :
        verbose_name = u"Страницы"

class AbstractSettings(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(AbstractSettings, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()

class PagesSettings(AbstractSettings):

    site_name = models.CharField(
        max_length=255, 
        verbose_name=u"Название сайта"
    )

    copyright = models.CharField(
        max_length=255, 
        verbose_name=u"Копирайт", 
        null=True, 
        blank=True
    )

    top_menu = models.ManyToManyField(
        Page, 
        null=True, 
        blank=True, 
        verbose_name=u"Верхнее меню", 
        related_name="+tm"
    )
    
    bottom_menu = models.ManyToManyField(
        Page, 
        null=True, 
        blank=True, 
        verbose_name=u"Нижнее меню", 
        related_name="+bm"
    )
    
    jumbotron_h = models.CharField(
        max_length=128,
        null=True,
        blank=True, 
        verbose_name=u"Джамб-название"
    )
    
    jumbotron_p = models.CharField(
        max_length=255,
        null=True,
        blank=True, 
        verbose_name=u"Джамб-предложение"
    )
    
    def get_default_copyright(self):
        return "%s (c) %s" % (str(date.today().year), str("Copyright"))
    
    def __unicode__(self):
        return u"Настройки"
    
    class Meta :
        verbose_name = u"Настройки"
