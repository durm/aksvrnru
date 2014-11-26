#-*- coding: utf-8 -*-

from django import template
from rubrics.models import Rubric
from products.models import Product

register = template.Library()

def get_products_count(rubric):
    all_children = rubric.get_all_published_children()
    products = Product.get_published_products().filter(Q(rubrics__in=all_children)|Q(rubrics__in=[rubric]))
    return len(products)
    
register.filter('products_count', get_products_count)
