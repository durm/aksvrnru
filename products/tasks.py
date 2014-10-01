#-*- coding: utf-8 -*-

from __future__ import absolute_import
from celery import shared_task
from django.shortcuts import render
from products.models import *
from aksvrnru import settings
import os
import traceback
from lxml import html, etree
import uuid
import urllib
import xlrd
from multiprocessing.pool import ThreadPool
from django.core.urlresolvers import reverse
from products.models import Price
from django.contrib.auth.models import User

CHILD_RUBRIC_COLOR = 23
PARENT_RUBRIC_COLOR = 63
SPECIAL_PRICE = 40
IS_NEW = 42
RECOMMEND_PRICE = 10

def get_path(fpath):
    return os.path.join(settings.MEDIA_ROOT, fpath)

def get_row_values(ws, row):
    return ws.row_values(row, start_colx=0, end_colx=6)

def get_prop(r, i):
    return r[i]

def is_empty_row(r):
    return is_empty(get_prop(r, 0))

def get_name(r):
    return get_prop(r, 0)

def get_trade_price(r):
    return get_prop(r, 1)

def get_retail_price(r):
    return get_prop(r, 2)

def get_by_order(r):
    return False

def get_amount(r):
    return 0

def get_external_link(ws, row):
    link = ws.hyperlink_map.get((row, 5))

    if link is not None :
        return link.url_or_path
    else:
        return ""

def update_external_link(ws, row, uri):
    link = ws.hyperlink_map.get((row, 5))

    if link is not None :
        link.url_or_path = uri

def is_empty(x):
    return x == ""

def is_rubric(r):
    return not(is_empty(get_prop(r, 0))) and is_empty(get_prop(r, 1)) and is_empty(get_prop(r, 2)) and is_empty(get_prop(r, 5))

def is_product(r):
    return not(is_empty(get_prop(r, 0))) and not(is_empty(get_prop(r, 1))) and not(is_empty(get_prop(r, 2))) and not(is_empty(get_prop(r, 5)))

def is_by_order(v):
    return v == u"Под заказ"

def is_double_dash(v):
    return v == u"--"

def get_trade_price_and_is_by_order(trade_price):
    if is_by_order(trade_price) :
        return (0, True)
    else:
        return (get_float(trade_price), False)

def get_float(v):
    try:
        return float(v)
    except:
        return 0

def make_stats():
    return {"products": 0, "rubrics": 0}

def inc_products(stats):
    stats["products"] += 1

def inc_rubrics(stats):
    stats["rubrics"] += 1

def is_main_rubric(wb, ws, row):
    cell = ws.cell(row, 0)
    xs_ind = cell.xf_index
    xf = wb.xf_list[xs_ind]
    return xf.background.pattern_colour_index == PARENT_RUBRIC_COLOR

def is_child_rubric(wb, ws, row):
    cell = ws.cell(row, 0)
    xs_ind = cell.xf_index
    xf = wb.xf_list[xs_ind]
    return xf.background.pattern_colour_index == CHILD_RUBRIC_COLOR

def is_product_special_price(wb, ws, row):
    cell = ws.cell(row, 0)
    xs_ind = cell.xf_index
    xf = wb.xf_list[xs_ind]
    return xf.background.pattern_colour_index == SPECIAL_PRICE

def is_product_new(wb, ws, row):
    cell = ws.cell(row, 0)
    xs_ind = cell.xf_index
    xf = wb.xf_list[xs_ind]
    return xf.background.pattern_colour_index == IS_NEW

def is_price_recommend(wb, ws, row):
    cell = ws.cell(row, 2)
    xs_ind = cell.xf_index
    xf = wb.xf_list[xs_ind]
    return wb.font_list[xf.font_index].colour_index == RECOMMEND_PRICE

def parse_name(fullname, user):
    parts = fullname.split("|")
    parts = [i.strip() for i in parts]

    name = parts[1] if len(parts) >= 2 else ""

    vendor, created = Vendor.objects.get_or_create(name=parts[0]) if len(parts) >= 1 else ("", False)

    if created :
        vendor.created_by = user

    vendor.updated_by = user
    vendor.save()

    short_desc = parts[2] if len(parts) >= 3 else ""

    return (name, vendor, short_desc)

def store_rubric(r, user, parent=None):
    name = get_name(r)

    if parent is not None :
        rubric, created = Rubric.objects.get_or_create(name=name, parent=parent)
    else:
        rubric, created = Rubric.objects.get_or_create(name=name, parent__isnull=True)

    rubric.updated_by = user
    if created :
        rubric.is_published = True
        rubric.created_by = user

    rubric.save()
    return (rubric, created)

@shared_task
def update_product_with_external_desc(product):

    print "Update prd external desc %s" % str(product.id)

    if not product.external_link or product.desc : return

    product.desc = get_external_desc(product.external_link)
    product.save()

def store_product(rowValues, ws, row, user, current_rubric, wb):

    in_price_desc = get_name(rowValues)

    trade_price = get_trade_price(rowValues)
    retail_price = get_retail_price(rowValues)

    external_link = get_external_link(ws, row)

    name, vendor, short_desc = parse_name(in_price_desc, user)

    product, created = Product.objects.get_or_create(name=name)

    is_published = True if product.is_published or created else False

    created_by = user if created else None

    is_new = is_product_new(wb, ws, row)
    is_special_price = is_product_special_price(wb, ws, row)
    is_recommend_price = is_price_recommend(wb, ws, row)

    prd_by_order = is_by_order(trade_price) or is_by_order(retail_price)

    specify_trade_price = is_double_dash(trade_price)
    specify_retail_price = is_double_dash(retail_price)

    trade_price = get_float(trade_price)
    retail_price = get_float(retail_price)

    product_entry = {
        "in_price_desc": in_price_desc,
        "name": name,
        "vendor": vendor,
        "short_desc": short_desc,
        "external_link": external_link,
        "is_published": is_published,
        "created_by": created_by,
        "updated_by": user,
        "is_new": is_new,
        "is_special_price": is_special_price,
        "is_recommend_price": is_recommend_price,
        "current_rubric": current_rubric,
        "is_by_order": prd_by_order,
        "specify_retail_price": specify_retail_price,
        "specify_trade_price": specify_trade_price,
        "trade_price": trade_price,
        "retail_price": retail_price,
    }

    product.store(product_entry)

    update_external_link(ws, row, reverse('get_product', kwargs={'num':product.id}))

    update_product_with_external_desc.delay(product)

@shared_task
def proc(request, obj):
    
    user = User.objects.get(id=user)
    obj = Price.objects.get(id=obj)
    
    if obj.processed() or obj.processing() : return

    Product.objects.all().update(available = False)

    obj.set_processing()

    try:
        stats = parse_xlsx_xlrd(get_path(obj.file.name), request)

        obj.set_success_result(request.user, get_success_desc(stats))
    except Exception as e:
        print traceback.print_exc()
        obj.set_error_result(request.user, str(e))

def parse_xlsx_xlrd(f, request):

    wb = xlrd.open_workbook(f, formatting_info=True)
    ws = wb.sheet_by_index(0)

    current_rubric = None
    parent = None

    stats = make_stats()

    for row in range(ws.nrows)[4:]:
        rowValues = get_row_values(ws, row)

        if is_empty_row(rowValues) :
            break
        if is_rubric(rowValues) :

            if is_main_rubric(wb, ws, row) :
                parent = None

            if is_child_rubric(wb, ws, row) :
                pass

            current_rubric, created = store_rubric(rowValues, request.user, parent)
            if is_main_rubric(wb, ws, row) :
                parent = current_rubric

            inc_rubrics(stats)
        if is_product(rowValues):

            if current_rubric.skip :
                continue
                pass

            store_product(rowValues, ws, row, request.user, current_rubric, wb)
            inc_products(stats)

    return stats

def get_success_desc(stats):
    return "Прайс успешно обработан. (рубрики: %s, продукты: %s)" % (stats.get("rubrics",0), stats.get("products", 0))
