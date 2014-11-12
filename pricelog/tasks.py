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
from products.models import Product
from datetime import datetime
import traceback

def proc(price):
    try:
        xmlprice = xls_to_xml_by_path(price.name)
        
        products = Product.objects.all().update(available_for_trade=False, available_for_retail=False)
        #set_products_unavailable(products)
        
        store_rubrics(xmlprice)
        link_rubrics(xmlprice)
        store_documents(xmlprice)
        
        price.desc = ""
        price.result = "success"
        price.save()
    except Exception as e:
        price.desc = "[%s] Error: %s %s" % (datetime.now(), str(e), traceback.format_exc())
        price.result = "error"
        price.save()
    finally:
        os.remove(price.name)

def store_rubrics(xmlprice):
    for c, item in enumerate(xmlprice.xpath(".//rubric[@hashsum]")):
        try:
            rubric = Rubric.objects.get(hashsum=item.get("hashsum"))
            if rubric.skip :
                continue
        except Rubric.DoesNotExist :
            rubric = Rubric.objects.create(hashsum=item.get("hashsum"))
            rubric.is_published = True

        rubric.name = item.get("name")
        rubric.colour_index = item.get("colour_index")
        rubric.save()
        print "%s) store_rubric %s" % (str(c), item.get("name"))

def link_rubrics(xmlprice):
    for c, item in enumerate(xmlprice.xpath(".//rubric[@hashsum]")):
        try:
            rubric = Rubric.objects.get(hashsum=item.get("hashsum"))
        except Rubric.DoesNotExist :
            print "-- error rubric does not exist %s" % item.get("hashsum")
            continue
        
        parent = None
        parent_item = item.getparent()
        if parent_item is not None and "hashsum" in parent_item.attrib :
            try:
                parent = Rubric.objects.get(hashsum=parent_item.get("hashsum"))
            except Rubric.DoesNotExist :
                print "-- error rubric does not exist %s" % item.get("hashsum")
                
        rubric.parent = parent
        rubric.save()
        
        print "%s) link_rubrics %s to %s" % (str(c), item.get("name", ""), parent_item.get("name", "") if parent_item is not None else "None")
        
def store_documents(xmlprice):
    for c, item in enumerate(xmlprice.xpath(".//product")) :
        parent = None 
        parent_node = item.getparent()
        if parent_node is not None and "hashsum" in parent_node.attrib :
            try:
                parent = Rubric.objects.get(hashsum=parent_node.get("hashsum"))
            except Rubric.DoesNotExist :
                continue
        else:
            continue
        try:
            store_product(item, parent)
            print "%s) store_document %s" % (str(c), item.get("name", ""))
        except Exception as e:
            print "-- error with %s: %s" % (item.get("name"), str(e))

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
