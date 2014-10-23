#-*- coding: utf-8 -*-

from django.db import models
from utils.models import Proto

price_parsing_result = (
    ('success', u"Успешно"),
    ('error', u"Ошибка"),
    ('process', u"В процессе"),
)

class Price(Proto):

    result = models.CharField(
        choices = price_parsing_result, 
        verbose_name = u"Статус",
        max_length = 32
    )

    class Meta :
        verbose_name = u"Прайс"
