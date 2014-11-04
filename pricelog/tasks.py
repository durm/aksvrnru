#-*- coding: utf-8 -*-

from products.models import Product
from aksvrnru import settings
import os
import traceback
from lxml import html, etree
import uuid
import urllib
import xlrd
from django.core.urlresolvers import reverse
from pricelog.models import Price
from django.contrib.auth.models import User
from xlstools.xlstoxml import xls_to_xml_by_path
from rubrics.models import Rubric
from vendors.models import Vendor
from datetime import datetime

def proc(price):
    try:
        xmlprice = xls_to_xml_by_path(price.name)
        store_rubric(xmlprice)
        price.desc = ""
        price.result = "success"
        price.save()
    except Exception as e:
        price.desc = str(e)
        print "[%s] Error: %s" % (datetime.now(), str(e))
        price.result = "error"
        price.save()
    finally:
        os.remove(price.name)

def store_rubric(item, parent=None) :
    
    current_rubric = parent 
    if item.get("hashsum") :
        try:
            rubric = Rubric.objects.get(hashsum=item.get("hashsum"))
            if rubric.skip :
                return
        except Rubric.DoesNotExist :
            rubric = Rubric.objects.create(hashsum=item.get("hashsum"))

        rubric.name = item.get("name")
        rubric.parent = parent
        rubric.save()
        current_rubric=rubric
 
    for child in item :
        if child.tag == "rubric" :
            current_rubric = store_rubric(child, current_rubric)
        if child.tag == "product" :
            store_product(child, current_rubric)

def store_product(item, parent):
    vendor_name = item.get("vendor")
    vendor, created = Vendor.objects.get_or_create(name=vendor_name)

    product, created = Product.objects.get_or_create(name=item.get("name"), vendor=vendor)
    product.short_desc = item.get("short_desc")
    product.trade_by_order = item.get("trade_by_order") == "1"
    product.available_for_trade = item.get("available_for_trade") == "1"    
    product.available_for_retail = item.get("available_for_retail") == "1"
    if product.available_for_trade and not product.trade_by_order :
        product.trade_price = float(item.get("trade_price", 0))
    if product.available_for_retail :
        product.retail_price = float(item.get("retail_price", 0))
    product.is_recommend_price = item.get("is_recommend_price") == "1"
    product.is_new = item.get("is_new") == "1"
    product.is_special_price = item.get("is_special_price") == "1"
    
    product.external_link = item.get("external_link")

    product.is_published = created or product.is_published

    product.rubrics.add(parent)

    product.save()
