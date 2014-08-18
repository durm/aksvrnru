#-*- coding: utf-8 -*-

from django.shortcuts import render
from products.models import *
from aksvrnru import settings
import os
from openpyxl import load_workbook
import traceback
from lxml import html, etree
import uuid
import urllib
import xlrd

def get_path(fpath):
    return os.path.join(settings.MEDIA_ROOT, fpath)

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

def proc(request, obj):

    if obj.processed() or obj.processing() :
        return

    obj.set_processing()

    obj.result_desc = ""

    obj.save()

    #try:
    stats = parse_xlsx_xlrd(get_path(obj.file.name), request)

    obj.set_success_result(get_success_desc(stats))
    #except Exception as e:

    #    raise e

    #    tb = traceback.print_exc()
    #    tb = " (" + tb + ")" if tb is not None else ""

    #    obj.set_error_result(str(e) + tb)

    obj.set_processed(request.user)

    obj.save()

def parse_xlsx_xlrd(f, request):

    wb = xlrd.open_workbook(f, formatting_info=True)
    ws = wb.sheet_by_index(0)

    current_rubric = None

    stats = {'rubrics':0, 'products':0}

    for row in range(ws.nrows)[4:]:

        rowValues = ws.row_values(row, start_colx=0, end_colx=5)

        name = rowValues[0]

        if not name : break

        trade_price = rowValues[1]
        retail_price = rowValues[2]

        link = ws.hyperlink_map.get((row, 5))

        if link is not None :
            external_link = link.url_or_path
        else:
            external_link=""

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

            if link is not None :
                product.external_link = link.url_or_path

                product.desc = get_html_desc(product.external_link)

            product.created_by=request.user
            product.updated_by=request.user

            product.rubrics.add(current_rubric)

            product.save()

            stats["products"] += 1

    return stats

def get_success_desc(stats):
    return "Прайс успешно обработан. (рубрики: %s, продукты: %s)" % (stats.get("rubrics",0), stats.get("products", 0))
