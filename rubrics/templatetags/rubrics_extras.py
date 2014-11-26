#-*- coding: utf-8 -*-

from django import template
from rubrics.models import Rubric
from products.models import Product
from django.db.models import Q

register = template.Library()

@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    request = context['request']
    updated = request.GET.copy()
    if "page" in updated :
        qd.pop('page')
    updated.update(kwargs)
    return updated.urlencode()
    
