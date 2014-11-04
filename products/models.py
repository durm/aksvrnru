#-*- coding: utf-8 -*-

from django.db import models
from utils.models import Proto
from vendors.models import Vendor
from entities.models import Entity
from rubrics.models import Rubric

sale_rate = (
    (0, '0%'),
    (0.1, '10%'),
    (0.2, '20%'),
    (0.3, '30%'),
    (0.4, '40%'),
    (0.5, '50%'),
    (0.6, '60%'),
    (0.7, '70%'),
    (0.8, '80%'),
    (0.9, '90%'),
)

class Product(Proto) :

    vendor = models.ForeignKey(
        Vendor, 
        verbose_name=u"Производитель", 
        null=True, 
        blank=True
    )

    short_desc = models.TextField(
        blank=True, 
        null=True, 
        verbose_name=u"Краткое описание"
    )

    entities = models.ManyToManyField(
        Entity, 
        blank=True, 
        null=True, 
        verbose_name=u"Картинки"
    )

    trade_price = models.FloatField(
        default=0, 
        verbose_name=u"Оптовая цена"
    )

    retail_price = models.FloatField(
        default=0, 
        verbose_name=u"Розничная цена"
    )
    
    available_for_trade = models.BooleanField(
        default=False, 
        verbose_name=u"Доступен для опта"
    )

    available_for_retail = models.BooleanField(
        default=False, 
        verbose_name=u"Доступен для розницы"
    )

    is_recommend_price = models.BooleanField(
        default=False, 
        verbose_name=u"Рекомендованная цена"
    )

    amount = models.IntegerField(
        default=0, 
        verbose_name=u"Количество"
    )

    external_link = models.URLField(
        blank=True, 
        null=True, 
        verbose_name=u"Внешняя ссылка"
    )

    trade_by_order = models.BooleanField(
        default=False, 
        verbose_name=u"Опт под заказ"
    )

    is_new = models.BooleanField(
        default=False, 
        verbose_name=u"Новое поступление"
    )

    is_special_price = models.BooleanField(
        default=False, 
        verbose_name=u"Спец. цена"
    )

    rubrics = models.ManyToManyField(
        Rubric, 
        blank=True, 
        null=True, 
        verbose_name=u"Рубрики"
    )

    is_valid = models.BooleanField(
        default=False, 
        verbose_name=u"Валиден"
    )

    is_published = models.BooleanField(
        default=False, 
        verbose_name=u"Опубликован"
    )

    """
    sale = models.FloatField(choices=sale_rate, blank=True, null=True, verbose_name="Скидка")
 
    @staticmethod
    def subset_by_rubrics(r, c = 6):
        return Product.objects.filter(is_published=True, rubrics__in=r.all()).order_by('?')[:c]
    
    @staticmethod
    def subset_of_special_price(c = 6):
        return Product.objects.filter(is_published=True, is_special_price=True).order_by('?')[:c]
    """

    class Meta :
        verbose_name = "Продукт"
