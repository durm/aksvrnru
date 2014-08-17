#-*- coding: utf-8 -*-

from django.shortcuts import render
from products.models import *
from aksvrnru import settings
import os
from openpyxl import load_workbook


SUCCESS_DESC = "Прайс успешно обработан"

def get_path(fpath):
    return os.path.join(settings.MEDIA_ROOT, fpath)

def proc(request, obj):

    #if obj.is_processed :
    #    return

    try:
        stats = parse_xlsx(get_path(obj.file.name), request)

        obj.result = price_parsing_result[0][0]
        obj.result_desc = SUCCESS_DESC + " (рубрики: %s, продукты: %s)" % (stats.get("rubrics",0), stats.get("products", 0))
    except Exception as e:
        obj.result = price_parsing_result[1][0]
        obj.result_desc = str(e)
        print "Exceptiion:", str(e)

    obj.processed_by = request.user
    obj.is_processed = True

    obj.save()

def get_prop(r, i):
    return r[i].value

def get_name(r):
    return get_prop(r, 0)

def get_trade_price(r):
    return get_prop(r, 1)

def get_retail_price(r):
    return get_prop(r, 2)

def get_by_order(r):
    #return get_prop(r, 3)
    return False

def get_amount(r):
    #return get_prop(r, 4)
    return 0

def get_external_link(r):
    return get_prop(r, 5)

def is_empty(x):
    return x == ""

def is_rubric(tp, rp, e):
    return is_empty(tp) and is_empty(rp) and is_empty(e)

def is_by_order(v):
    return v == u"Под заказ"

def get_float(v):
    try:
        return float(v)
    except:
        return 0

def parse_xlsx(f, request):

    wb = load_workbook(filename = f)
    ws = wb.active

    current_rubric = None

    stats = {'rubrics':0, 'products':0}

    for row in ws.rows[4:]:

        name = get_name(row)

        if not name : break

        trade_price = get_trade_price(row)
        retail_price = get_retail_price(row)
        external_link = get_external_link(row)

        if is_rubric(trade_price, retail_price, external_link) :

            current_rubric, created = Rubric.objects.get_or_create(name=name)
            stats["rubrics"] += 1

        else:

            product, created = Product.objects.get_or_create(name=name)

            if is_by_order(trade_price) :
                product.by_order = True
                product.trade_price=0
            else:
                product.trade_price = get_float(trade_price)

            product.retail_price=get_float(retail_price)

            product.created_by=request.user
            product.updated_by=request.user

            product.rubrics.add(current_rubric)

            product.save()

            stats["products"] += 1

    return stats
