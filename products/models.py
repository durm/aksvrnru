#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete, post_save
from django.dispatch.dispatcher import receiver
import os
from aksvrnru.utils import *
from aksvrnru import settings

price_parsing_result = (
    ('success', 'Успешно'),
    ('error', 'Ошибка'),
    ('process', 'В процессе'),
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
    result_desc = models.TextField(blank=True, null=True, verbose_name="Сводка")

    def processed(self):
        return self.is_processed
    
    def processing(self):
        return not self.processed() and self.result == price_parsing_result[2][0]
    
    def set_processing(self):
        self.result = price_parsing_result[2][0]
        
    def set_success_result(self, desc):
        self.result = price_parsing_result[0][0]
        self.result_desc = desc
        
    def set_error_result(self, desc):
        self.result = price_parsing_result[1][0]
        self.result_desc = desc

    def set_processed(self, user):
        self.is_processed = True
        self.processed_by = user

    def __unicode__(self):
        name = self.name if self.name else self.file.name
        return "%s #%s" % (name, self.id)

    class Meta :
        verbose_name = "Прайс"

class Rubric(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название", unique=True)
    desc = models.TextField(blank=True, verbose_name="Описание")
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name="Родительская рубрика")

    def __unicode__(self):
        return "%s #%s" % (self.name, self.id)

    class Meta :
        verbose_name = "Рубрика"

class Product(models.Model) :

    name = models.CharField(max_length=255, verbose_name="Название", unique=True)
    desc = models.TextField(blank=True, verbose_name="Описание")

    image = models.ImageField(upload_to='products', verbose_name="Изображение", null=True, blank=True)

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

    rubrics = models.ManyToManyField(Rubric, blank=True, null=True, verbose_name="Рубрики")

    def __unicode__(self):
        return "%s #%s" % (self.name, self.id)
    
    def has_image(self):
        return self.image is not None
    
    def get_full_image_path(self):
        if self.has_image() :
            return os.path.join(settings.MEDIA_ROOT, self.image.name)

    def create_product_thumbnails(self):
        if self.has_image() :
            fpath = self.get_full_image_path()
            
            fpath200 = "%s200" % fpath
            get_thumbnail(fpath, (250,250), fpath200)
            add_watermark(fpath200, settings.WATER_MARK, fpath200)
            
            fpath500 = "%s500" % fpath
            get_thumbnail(fpath, (500,500), fpath500)
            add_watermark(fpath500, settings.WATER_MARK, fpath500)
            
            add_watermark(fpath, settings.WATER_MARK, fpath)
        
    def delete_thumbnails(self):
        if self.has_image() :
            fpath = self.get_full_image_path()
            os.remove("%s200" % fpath)
            os.remove("%s500" % fpath)

    class Meta :
        verbose_name = "Продукт"

@receiver(pre_delete, sender=Product)
def _product_delete_pre(sender, instance, **kwargs):
    instance.delete_thumbnails()
    
@receiver(post_save, sender=Product)
def _product_create_post(sender, instance, **kwargs):
    instance.create_product_thumbnails()