#-*- coding: utf-8 -*-

from django import template
from rubrics.models import Rubric
from products.models import Product
from django.db.models import Q

register = template.Library()

def get_products_count(rubric):
    all_children = rubric.get_all_published_children()
    products = Product.get_published_products().filter(Q(rubrics__in=all_children)|Q(rubrics__in=[rubric]))
    return len(products)
    
@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    updated.update(kwargs)
    return updated.urlencode
    
register.filter('products_count', get_products_count)
