#-*- coding: utf-8 -*-

from django.shortcuts import redirect, render_to_response
from products.models import Rubric, Product
from pages.views import get_context
from django.contrib.auth import authenticate
from aksvrnru.views import error
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login

def rubrics_hierarchy(request, choose=False, tpl='hierarchy/hierarchy.html'):
    rubrics = Rubric.objects.filter(parent__isnull=True)
    return render_to_response(tpl, {"rubrics":rubrics, "choose":choose}, get_context(request))

def get_product(request, num):
    try:
        product = Product.objects.get(id=num)
        return render_product(request, product)
    except Product.DoesNotExist :
        return page_doesnot_exist(request, num)

def render_product(request, product):
    return render_to_response("products/product.html", {'product':product}, get_context(request))

def get_rubrics_hierarchy_for_upload(request):
    return rubrics_hierarchy(request, choose=True, tpl='hierarchy/construct_price.html')
