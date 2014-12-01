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
    
    image = models.ImageField(
        upload_to=u"rubrics", 
        verbose_name=u"Картинка",
        null=True, 
        blank=True
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
        
    def get_all_published_children(self):
        def iter_func(rubric, l):
            for c in rubric.get_published_children() :
                print c
                l += [c]
                l = iter_func(c, l)
            return l
        return iter_func(self, [])    
    
    def rubricator_path(self):
        def add_to_path(rubric, path):
            if rubric is None : return path
            return add_to_path(rubric.parent, path + [rubric])
        rev_path = add_to_path(self.parent, [self])
        rev_path.reverse()
        return rev_path

    def to_xml(self):
        """<rubric name="%s" colour_index="%s" hashsum="%s">"""
        rxml = etree.Element("rubric")
        rxml.set("name", self.name)
        rxml.set("colour_index", self.colour_index)
        rxml.set("hashsum", self.hashsum)
        return rxml

    class Meta :
        verbose_name = u"Рубрика"
    
    
