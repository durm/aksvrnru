#-*- coding: utf-8 -*-

from django.shortcuts import redirect, render_to_response, render
from products.models import Product
from vendors.models import Vendor
from rubrics.models import Rubric
from utils.views import get_context
from django.contrib.auth import authenticate
from aksvrnru.views import error, message
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
import xlwt
import StringIO, tempfile
import uuid
from django.http import HttpResponse, QueryDict
from datetime import datetime
from aksvrnru import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from lxml import etree
from pricelog.xlstools.xmltoxls import xml_to_xls

def rubrics_hierarchy(request, choose=False, tpl='products/hierarchy.html', is_published=True):
    rubrics = Rubric.objects.filter(parent__isnull=True, is_published=True)
    if rubrics.count() :
        return render_to_response(tpl, {"rubrics":rubrics, "choose":choose, "sale_rate": None}, get_context(request))
    else:
        return message(request, u"Нет активных рубрик!", u"")

def proc_price_param(p):
    try:
        p = float(p.replace(",", "."))
    except:
        p = ""
    return p

def listing(request):
    
    vendors = Vendor.objects.all()
    rubrics = Rubric.get_published_rubrics()
    
    q_filter = request.GET.get("q", "")
    
    price_from_filter = proc_price_param(request.GET.get("price_from", ""))
    price_to_filter = proc_price_param(request.GET.get("price_to", ""))
    
    available_filter = request.GET.get("a", "") == "1"
    
    vendor_filter = request.GET.getlist("vendor", None)
    rubric_filter = request.GET.getlist("rubric", None)
    
    products = Product.objects.filter(is_published=True)
    
    if price_from_filter :
        products = products.filter(retail_price__gt=price_from_filter)
    if price_to_filter :
        products = products.filter(retail_price__lt=price_to_filter)    
    if q_filter :
        products = products.filter(Q(short_desc__icontains=q_filter)|Q(name__icontains=q_filter)|Q(desc__icontains=q_filter)|Q(vendor__name__icontains=q_filter))   
    if available_filter :
        products = products.filter(available_for_retail=available_filter)
    if vendor_filter :
        products = products.filter(vendor__in=vendor_filter)
    if rubric_filter :
        
        rubrics_id = []
        rubrics_id += rubric_filter
        
        rubrics = Rubric.objects.filter(id__in=rubric_filter)
        for rubric in rubrics :
            get_children_ids(rubrics_id, rubric)
        
        products = products.filter(rubrics__in=rubrics_id)
    
    order_by = request.REQUEST.get("order_by", "")
    direction = request.REQUEST.get("direction", "")
    direction = "-" if direction == "-" else ""
    if order_by in ["vendor__name", "id", "retail_price"] :
        products = products.order_by(direction + order_by)
    else:
        order_by = None
    
    products_count = products.count()
    paginator = Paginator(products, 25)
    
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
        
    qparams = {
        'q_filter':q_filter, 
        'vendor_filter': map(id_to_int, vendor_filter), 
        'rubric_filter': map(id_to_int, rubric_filter), 
        'price_from_filter':price_from_filter, 
        'price_to_filter':price_to_filter, 
        'available_filter':available_filter
    }
    
    qd = request.GET.copy()
    
    if "page" in qd :
        qd.pop('page')
        
    if "order_by" in qd :
        qd.pop('order_by')
        
    req = {
        "products": products, 
        "direction":direction, 
        "order_by": order_by, 
        "qparams":qparams, 
        "qparams_str":qd.urlencode(), 
        "product_count":products_count,
        "vendors": vendors,
        "rubrics": rubrics
    }
    
    return render_to_response('products/list.html', req, get_context(request))

def get_children_ids(l, rubric):
    for c in rubric.children():
        l.append(c.id)
        get_children_ids(l, c)

def id_to_int(i):
    try:
        return int(i)
    except:
        return None

# get product page
def get_product(request, num):
    try:
        product = Product.objects.get(id=num)
        
        return render_product(request, product)
    except Product.DoesNotExist :
        return error(request, u"Нет продукта с таким идентификатором!", u"")

# product renderer
def render_product(request, product):
    return render_to_response("products/product.html", {'product':product}, get_context(request))

def get_rubrics_hierarchy_for_upload(request):
    rubrics = Rubric.objects.filter(parent__isnull=True, is_published=True).count()
    if rubrics == 0 :
        return message(request, u"Нет активных рубрик!", u"Нельзя сгенерировать прайс!")
    return rubrics_hierarchy(request, choose=True, tpl='products/construct_price.html')

def build_price_xml(xml, rubric_ids, rubrics):
    for rubric in rubrics :
        rxml = rubric.to_xml()
        build_price_xml(rxml, rubric_ids, rubric.get_published_children().filter(id__in=rubric_ids))
        for product in Product.objects.filter(rubrics__in=[rubric], is_published=True) :
            rxml.append(product.to_xml())
        xml.append(rxml)

def construct_price(request):
    rubric_ids = request.POST.getlist("rubric")
    
    price = etree.Element("price")
    parents = Rubric.objects.filter(id__in=rubric_ids, parent=None)
    
    build_price_xml(price, rubric_ids, parents) 

    myfile = StringIO.StringIO()

    xls = xml_to_xls(price)
    xls.save(myfile)
    
    response = HttpResponse(myfile.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=myfile.xls'
    response['Content-Length'] = myfile.tell()
    return response
    
# get product url
def get_product_url(product, domain):
    return xlwt.Formula(u'HYPERLINK("%s%s";"На сайте...")' % (domain, reverse('get_product', kwargs={'num':product.id})))
