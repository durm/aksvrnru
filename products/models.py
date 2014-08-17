#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

price_parsing_result = (
    ('success', 'Успешно'),
    ('error', 'Ошибка'),
)

class Price(models.Model):

    name = models.CharField(max_length=255, verbose_name="Название", unique=True)
    desc = models.TextField(blank=True, verbose_name="Описание")

    file = models.FileField(upload_to='prices', verbose_name="Файл")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    created_by = models.ForeignKey(User, related_name='+cr+', blank=True, null=True, verbose_name="Создал")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    updated_by = models.ForeignKey(User, related_name='+up+', blank=True, null=True, verbose_name="Изменил")

    is_processed = models.BooleanField(default=False, verbose_name="Обработан")
    processed_at = models.DateTimeField(auto_now=True, verbose_name="Дата обработки")
    processed_by = models.ForeignKey(User, related_name='+pr+', blank=True, null=True, verbose_name="Инициатор обработки")

    result = models.CharField(max_length=7, choices=price_parsing_result, blank=True, verbose_name="Результат")
    result_desc = models.TextField(blank=True, verbose_name="Сводка")

    def __unicode__(self):
        name = self.name if self.name else self.file.name
        return "%s #%s" % (name, self.id)

    class Meta :
        verbose_name = "Прайс"

class Rubric(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название", unique=True)
    desc = models.TextField(blank=True, verbose_name="Описание")

    def __unicode__(self):
        return "%s #%s" % (self.name, self.id)

    class Meta :
        verbose_name = "Рубрика"

class Product(models.Model) :

    name = models.CharField(max_length=255, verbose_name="Название", unique=True)
    desc = models.TextField(blank=True, verbose_name="Описание")

    trade_price = models.FloatField(default=0, verbose_name="Оптовая цена")
    retail_price = models.FloatField(default=0, verbose_name="Розничная цена")
    recommend_price = models.FloatField(default=0, verbose_name="Рекомендованная цена")

    amount = models.IntegerField(default=0)

    external_link = models.URLField(blank=True, verbose_name="Внешняя ссылка")

    by_order = models.BooleanField(default=False, verbose_name="Под заказ")

    is_new = models.BooleanField(default=False, verbose_name="Новое поступление")
    is_special_price = models.BooleanField(default=False, verbose_name="Спец. цена")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    created_by = models.ForeignKey(User, related_name='+cr+', blank=True, null=True, verbose_name="Создал")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    updated_by = models.ForeignKey(User, related_name='+up+', blank=True, null=True, verbose_name="Изменил")

    rubrics = models.ManyToManyField(Rubric, blank=True, verbose_name="Рубрики")

    def __unicode__(self):
        return "%s #%s" % (self.name, self.id)

    class Meta :
        verbose_name = "Продукт"
