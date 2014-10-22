#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from utils.models import Proto

class Rubric(Proto):

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

    """
    def get_products(self):
        return Product.objects.filter(rubrics__in=[self])

    def get_published_products(self):
        return self.get_products().filter(is_published=True)
    """

    class Meta :
        verbose_name = u"Рубрика"


