#-*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, RequestContext
from aksvrnru.views import error
from pages.models import Page, PagesSettings
from products.models import *
from utils.views import get_context

def home(request):
    special_price_products = None #Product.subset_of_special_price()

    req = {
        "special_price_products": special_price_products
    }
    #return render("1")
    return render_to_response("common/landing.html", req, get_context(request))

def get_page(request, num=1):
    try:
        page = Page.objects.get(id=num)
        return render_page(request, page)
    except Page.DoesNotExist :
        return page_doesnot_exist(request, num)

def render_page(request, page):
    return render_to_response("pages/page.html", {'page':page}, get_context(request))

def page_doesnot_exist(request, num):
    return error(request, u"Страница недоступна", u"Страница с идентификатором %s недоступна" % str(num))


