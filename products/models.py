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

    retail_price_in_price = models.FloatField(
        null=True,
        blank=True, 
        verbose_name=u"Розничная цена в прайсе"
    )

    retail_price_prev = models.FloatField(
        null=True,
        blank=True, 
        verbose_name=u"Прежняя розн. цена"
    )

    specify_trade_price = models.BooleanField(
        default=False, 
        verbose_name=u"Уточните опт. цену"
    )

    specify_retail_price = models.BooleanField(
        default=False, 
        verbose_name=u"Уточните розн. цену"
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

    by_order = models.BooleanField(
        default=False, 
        verbose_name=u"Под заказ"
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

    available = models.BooleanField(
        default=False, 
        verbose_name=u"В наличии"
    )
    
    #sale = models.FloatField(choices=sale_rate, blank=True, null=True, verbose_name="Скидка")
    """
    def get_full_image_path(self):
        if self.image :
            return os.path.join(settings.MEDIA_ROOT, self.image.name)

    def create_product_thumbnails(self):
        if self.image :
            fpath = self.get_full_image_path()

            fpath200 = "%s200" % fpath
            get_thumbnail(fpath, (250,250), fpath200)
            add_watermark(fpath200, settings.WATER_MARK, fpath200)

            fpath500 = "%s500" % fpath
            get_thumbnail(fpath, (500,500), fpath500)
            add_watermark(fpath500, settings.WATER_MARK, fpath500)

            add_watermark(fpath, settings.WATER_MARK, fpath)

    def get_retail_trade_diff(self):
        return self.retail_price - self.trade_price

    def validate(self):
        if self.by_order or ( self.trade_price == 0 or self.retail_price == 0 ) :
            return True
        else:
            return self.get_retail_trade_diff() >= 0

    def check_and_set_validation(self):
        self.is_valid = self.validate()
        if not self.is_valid :
            self.is_published = False

    def lower_then_minimal_retail_price(self):
        return self.retail_price < MIN_PRICE

    def lower_then_minimal_retail_trade_diff(self):
        return self.get_retail_trade_diff() < MIN_DIFF

    def skip_calculation(self):
        return not self.is_valid or self.is_recommend_price or ( self.trade_price == 0 or self.retail_price == 0 ) or self.lower_then_minimal_retail_price() or self.lower_then_minimal_retail_trade_diff()

    def calculate_retail_price(self):
        if self.skip_calculation() :
            return
        self.retail_price = self.get_retail_trade_diff() * PRICE_PERCENT + self.trade_price
        self.check_and_set_validation()

    def delete_thumbnails(self):
        if self.image :
            fpath = self.get_full_image_path()
            os.remove("%s200" % fpath)
            os.remove("%s500" % fpath)
            
    def same_rubric_products(self, c=6):
        return Product.subset_by_rubrics(self.rubrics, c)
    
    def price_with_sale(self, pr, sl):
        return pr - (pr * sl)
    
    def trade_price_with_sale(self, s=None):
        if s is None :
            s = self.sale if self.sale else 0
        else:
            s = float(s)
        return self.price_with_sale(self.trade_price, s)
    
    def retail_price_with_sale(self, s=None):
        if s is None :
            s = self.sale if self.sale else 0
        else:
            s = float(s)
        return self.price_with_sale(self.retail_price, s)

    def store(self, entry) :

        self.vendor = entry.get("vendor", None)

        self.name = entry.get("name","")
        self.short_desc = entry.get("short_desc", "")
        self.desc = entry.get("desc", "")

        self.trade_price = entry.get("trade_price", 0)

        self.retail_price_prev = self.retail_price
        self.retail_price = entry.get("retail_price", 0)
        self.retail_price_in_price = self.retail_price

        self.external_link = entry.get("external_link", "")

        self.is_new = entry.get("is_new", False)
        self.is_special_price = entry.get("is_special_price", False)

        self.is_published = entry.get("is_published", False)

        self.is_recommend_price = entry.get("is_recommend_price", False)

        self.by_order = entry.get("is_by_order", False)

        self.specify_retail_price = entry.get("specify_retail_price", False)
        self.specify_trade_price = entry.get("specify_trade_price", False)

        if entry.get("created_by", None) is not None :
            self.created_by = entry.get("created_by", None)

        self.updated_by = entry.get("updated_by", None)

        self.rubrics.add(entry.get("current_rubric", None))

        self.available = True

        self.check_and_set_validation()
        if self.is_valid :
            self.calculate_retail_price()

        self.save()

    def __unicode__(self):
        return "%s" % (self.name)
    
    @staticmethod
    def subset_by_rubrics(r, c = 6):
        return Product.objects.filter(is_published=True, rubrics__in=r.all()).order_by('?')[:c]
    
    @staticmethod
    def subset_of_special_price(c = 6):
        return Product.objects.filter(is_published=True, is_special_price=True).order_by('?')[:c]
    """

    class Meta :
        verbose_name = "Продукт"
