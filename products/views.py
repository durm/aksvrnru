#-*- coding: utf-8 -*-

from django.shortcuts import render
from products.models import *
from aksvrnru import settings
import os
import traceback
from lxml import html, etree
import uuid
import urllib
import xlrd

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

def is_empty(x):
    return x == ""

def is_rubric(r):
    return not(is_empty(get_prop(r, 0))) and is_empty(get_prop(r, 1)) and is_empty(get_prop(r, 2)) and is_empty(get_prop(r, 5))

def is_product(r):
    return not(is_empty(get_prop(r, 0))) and not(is_empty(get_prop(r, 1))) and not(is_empty(get_prop(r, 2))) and not(is_empty(get_prop(r, 5)))

def is_by_order(v):
    return v == u"Под заказ"

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
    
def is_main_rubric(wb, row):
    wb.xf_list[row[0].xf_index].background.pattern_colour_index == PARENT_RUBRIC_COLOR

def is_child_rubric(wb, row):
    wb.xf_list[row[0].xf_index].background.pattern_colour_index == CHILD_RUBRIC_COLOR
    
def is_product_special_price(wb, row):
    wb.xf_list[row[0].xf_index].background.pattern_colour_index == SPECIAL_PRICE
    
def is_product_new(wb, row):
    wb.xf_list[row[0].xf_index].background.pattern_colour_index == IS_NEW
    
def is_recommend_price(wb, row):
    return wb.font_list[wb.xf_list[row[2].xf_index].font_index].colour_index == RECOMMEND_PRICE

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
        rubric, created = Rubric.objects.get_or_create(name=name, parent__is_null=True)
    
    rubric.updated_by = user
    if created :
        rubric.created_by = user
        
    rubric.save()
    return (rubric, created)

def store_product(rowValues, ws, row, user, current_rubric, wb):

    name = get_name(rowValues)
    trade_price = get_trade_price(rowValues)
    retail_price = get_retail_price(rowValues)
    external_link = get_external_link(ws, row)

    name, vendor, short_desc = parse_name(name, user)

    trade_price, is_by_order = get_trade_price_and_is_by_order(trade_price)
    retail_price = get_float(retail_price)

    product, created = Product.objects.get_or_create(name=name)

    desc = get_external_desc(external_link) if external_link and created else ""

    created_by = user if created else None
    
    is_new, is_special_price = is_product_new(wb, row), is_product_special_price(wb, row)

    product.store(vendor=vendor,
                    short_desc=short_desc,
                    desc=desc,
                    trade_price=trade_price,
                    retail_price=retail_price,
                    external_link=external_link,
                    is_new = is_new,
                    is_special_price=is_special_price,
                    created_by=created_by,
                    updated_by=user,
                    current_rubric=current_rubric)

def proc(request, obj):

    #if obj.processed() or obj.processing() : return

    obj.set_processing()

    try:
        stats = parse_xlsx_xlrd(get_path(obj.file.name), request)

        obj.set_success_result(request.user, get_success_desc(stats))
    except Exception as e:

        tb = traceback.print_exc()
        tb = " (" + tb + ")" if tb is not None else ""
        obj.set_error_result(request.user, str(e) + tb)

def parse_xlsx_xlrd(f, request):

    wb = xlrd.open_workbook(f, formatting_info=True)
    ws = wb.sheet_by_index(0)

    current_rubric = None
    parent = None

    stats = make_stats()

    for row in range(ws.nrows)[4:20]:
        rowValues = get_row_values(ws, row)

        if is_empty_row(rowValues) :
            break
        if is_rubric(rowValues) :
            
            if is_main_rubric(wb, row) :
                parent = None
                
            if is_child_rubric(wb, row) :
                parent = current_rubric
            
            current_rubric, created = store_rubric(rowValues, request.user, parent)
            inc_rubrics(stats)
        if is_product(rowValues):
            store_product(rowValues, ws, row, request.user, current_rubric, wb)
            inc_products(stats)

    return stats

def get_success_desc(stats):
    return "Прайс успешно обработан. (рубрики: %s, продукты: %s)" % (stats.get("rubrics",0), stats.get("products", 0))
