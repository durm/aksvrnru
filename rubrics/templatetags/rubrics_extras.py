#-*- coding: utf-8 -*-

from django import template
from rubrics.models import Rubric
from products.models import Product
from django.db.models import Q

register = template.Library()

@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    updated.update(kwargs)
    return updated.urlencode
    
register.filter('products_count', get_products_count)
