#-*- coding: utf-8 -*-

from django.db import models

class Page(models.Model):
    title = models.CharField(max_length=255, verbose_name="Краткое название")
    name = models.TextField(verbose_name="Полное название")
    desc = models.TextField(blank=True, null=True, verbose_name="Описание")
    content = models.TextField(verbose_name="Содержание")
    parent = models.ForeignKey('self', blank=True, null=True, verbose_name="Родительская страница")

    def __unicode__(self):
        return self.name

    def has_children(self):
        return len(Page.objects.filter(parent=self)[:1]) == 1

    def children(self):
        return Page.objects.filter(parent=self)

    class Meta :
        verbose_name = "Страницы"

class AbstractSettings(models.Model):
    site_name = models.CharField(max_length=255, verbose_name="Название сайта")
    copyright = models.CharField(max_length=255, verbose_name="Копирайт")

    top_menu = models.ManyToManyField(Page, null=True, blank=True, verbose_name="Верхнее меню", related_name="+tm")
    bottom_menu = models.ManyToManyField(Page, null=True, blank=True, verbose_name="Нижнее меню", related_name="+bm")

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


    pass
