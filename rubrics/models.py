#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from utils.models import Proto
from lxml import etree

class Rubric(Proto):

    hashsum = models.CharField(
        max_length=50, 
        null=True, 
        blank=True,
        verbose_name=u"Хэш-сумма"
    )
    
    colour_index = models.CharField(
        max_length=50, 
        null=True, 
        blank=True,
        verbose_name=u"Код цвета"
    )

    parent = models.ForeignKey(
        "self",
        null=True, 
        blank=True, 
        verbose_name=u"Родительская рубрика"
    )

    is_published = models.BooleanField(
        default=False, 
        verbose_name=u"Опубликована"
    )

    skip = models.BooleanField(
        default=False, 
        verbose_name=u"Не обновлять из прайса"
    )

    def has_children(self):
        return len(Rubric.objects.filter(parent=self)[:1]) == 1 #lazy

    def children(self):
        return Rubric.objects.filter(parent=self)

    def get_published_children(self):
        return self.children().filter(is_published=True)
    
    @staticmethod
    def get_published_rubrics():
        return Rubric.objects.filter(is_published=True)
        
    """
    def get_products(self):
        return Product.objects.filter(rubrics__in=[self])

    def get_published_products(self):
        return self.get_products().filter(is_published=True)
    """
    
    def to_xml(self):
        """<rubric name="%s" colour_index="%s" hashsum="%s">"""
        rxml = etree.Element("rubric")
        rxml.set("name", self.name)
        rxml.set("colour_index", self.colour_index)
        rxml.set("hashsum", self.hashsum)
        return rxml

    class Meta :
        verbose_name = u"Рубрика"


