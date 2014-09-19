#-*- coding: utf-8 -*-

from django.shortcuts import redirect, render_to_response, render
from products.models import Rubric, Product
from pages.views import get_context
from django.contrib.auth import authenticate
from aksvrnru.views import error, message
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
import xlwt
import StringIO
import uuid
from django.http import HttpResponse

def rubrics_hierarchy(request, choose=False, tpl='hierarchy/hierarchy.html', is_published=True):
    rubrics = Rubric.objects.filter(parent__isnull=True, is_published=True)
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
    rubrics = Rubric.objects.filter(parent__isnull=True, is_published=True).count()
    if rubrics == 0 :
        return error(request, "Ошибка", "Нет активны рубрик! Нельзя сгенерировать прайс!")
    return rubrics_hierarchy(request, choose=True, tpl='hierarchy/construct_price.html')

def construct_price(request):
    price_type = request.POST.get("price_type")
    rubrics = request.POST.getlist("rubric")
    
    if price_type is None or len(rubrics) == 0 :
        return error(request, "Ошибка", "Не задан тип прайса или не выбраны рубрики")


    wb = xlwt.Workbook()
    ws = wb.add_sheet('Page1')
    
    rubrics = Rubric.objects.filter(parent__isnull=True, is_published=True)
    
    """
    r = 0
    for rubric in rubrics :
        write_rubric(ws, r, rubric)
        break
    """
    
    ws.write(0, 0, 1)
    
    f = StringIO.StringIO()
    
    wb.save(f)

    response = HttpResponse(f.read(), content_type="application/vnd.ms-excel")
    response['Content-Disposition'] = 'attachment; filename=price_%s.xls' % str(uuid.uuid4())
    return response

def write_rubric(ws, r, rubric):
    r += 1
    ws.write(r, 0, "bla")
    print rubric.name
    return
    products = Product.objects.filter(is_published=True, rubrics__in=[rubric.id])
    for product in products :
        r += 1
        write_product(ws, r, product)
    childs = rubric.children()
    for child in childs :
        r += 1
        write_rubric(ws, r, child)
        
def write_product(ws, r, product):
    ws.write(r, 0, product.name)
    
    