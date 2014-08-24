#-*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, RequestContext
from aksvrnru.views import error
from pages.models import Page, PagesSettings
from products.models import *

def home(request):
    special_price_products = Product.objects.filter(is_special_price=True).order_by('?')[:6]

    req = {
        "special_price_products": special_price_products
    }

    return render_to_response("pages/landing.html", req, get_context(request))

def get_page(request, num=1):
    try:
        page = Page.objects.get(id=num)
        return render_page(request, page)
    except Page.DoesNotExist :
        return page_doesnot_exist(request, num)

def render_page(request, page):
    return render_to_response("pages/page.html", {'page':page}, get_context(request))

def page_doesnot_exist(request, num):
    return error(request, "Страница недоступна", "Страница с идентификатором %s недоступна" % str(num))

def get_context(request):
    try:
        pages_settings = PagesSettings.objects.all()[0]
    except:
        pages_settings = None

    return RequestContext(request, {'pages_settings':pages_settings})
