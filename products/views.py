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
import StringIO, tempfile
import uuid
from django.http import HttpResponse
from datetime import datetime

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
    rubrics_ids = request.POST.getlist("rubric")
    
    if price_type is None or len(rubrics_ids) == 0 :
        return error(request, "Ошибка", "Не задан тип прайса или не выбраны рубрики")


    wb = xlwt.Workbook()
    ws = wb.add_sheet('Page1')
    
    rubrics = Rubric.objects.filter(parent__isnull=True, is_published=True, id__in=rubrics_ids)
    
    price_desc = u" для розницы " if price_type == "retail" else u" для розницы опта "
    
    style_string = "borders: top medium, bottom medium, left medium, right medium"
    style = xlwt.easyxf(style_string)
    
    ws.write(0, 0, u"Прайс%sсгенерирован %s" % (price_desc, str(datetime.now())))
    ws.write(1, 0, u"Наименование товара", style)
    ws.write(1, 1, u"Цена", style)
    ws.write(1, 2, u"Ссылка", style)
    
    col = ws.col(0)
    col.width = 1200 * 20
    
    r = 1
    for rubric in rubrics :
        r = write_rubric(ws, r, rubric, get_root_rubric_style())
    
    f = StringIO.StringIO()
    
    wb.save(f)

    response = HttpResponse(f.getvalue(), content_type="application/vnd.ms-excel")
    response['Content-Disposition'] = 'attachment; filename=price_%s.xls' % str(uuid.uuid4())
    return response

def write_rubric(ws, r, rubric, style=xlwt.XFStyle()):
    r += 1
    ws.write(r, 0, rubric.name, style)
    ws.write(r, 1, "", style)
    ws.write(r, 2, "", style)
    products = Product.objects.filter(rubrics__in=[rubric], is_published=True)
    for product in products :
        r = write_product(ws, r, product)
    childs = rubric.children()
    for child in childs :
        r = write_rubric(ws, r, child, get_rubric_stile())
    return r
        
def write_product(ws, r, product):
    r += 1
    style_string = "borders: bottom thin, left thin, right thin"
    style = xlwt.easyxf(style_string)
    
    ws.write(r, 0, "%s | %s | %s" % (product.vendor.name, product.name, product.short_desc), style)
    ws.write(r, 1, product.retail_price, style)
    ws.write(r, 2, u"На сайте...", style)
    return r

def get_rubric_stile(t="grey50"):
    style = xlwt.XFStyle()
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = xlwt.Style.colour_map[t]
    style.pattern = pattern
    style.font.colour_index = xlwt.Style.colour_map['white']
    style.font.bold = True
    return style

def get_root_rubric_style():
    return get_rubric_stile(t="grey80")
    