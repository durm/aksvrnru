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
from django.contrib.auth import authenticate, login
import xlwt
import StringIO, tempfile
import uuid
from django.http import HttpResponse, QueryDict
from datetime import datetime
from aksvrnru import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

def rubrics_hierarchy(request, choose=False, tpl='products/hierarchy.html', is_published=True):
    rubrics = Rubric.objects.filter(parent__isnull=True, is_published=True)
    if rubrics.count() :
        return render_to_response(tpl, {"rubrics":rubrics, "choose":choose, "sale_rate": sale_rate}, get_context(request))
    else:
        return message(request, u"Нет активных рубрик!", u"")

# listing for products
def listing(request):
    
    vendors = Vendor.objects.all()
    
    q_filter = request.GET.get("q", "")
    price_from_filter = request.GET.get("price_from", "")
    try:
        price_from_filter = float(price_from_filter.replace(",", "."))
    except:
        price_from_filter = ""
        
    price_to_filter = request.GET.get("price_to", "")
    try:
        price_to_filter = float(price_to_filter.replace(",", "."))
    except:
        price_to_filter = ""
    available_filter = request.GET.get("a", "") == "1"
    
    vendor_filter = request.GET.getlist("vendor", None)
    rubric_filter = request.GET.getlist("rubric", None)
    
    products = Product.objects.filter(is_published=True)
    
    if price_from_filter :
        products = products.filter(retail_price__gt=price_from_filter)
    if price_to_filter :
        products = products.filter(retail_price__lt=price_to_filter)    
    if q_filter :
        products = products.filter(Q(short_desc__contains=q_filter)|Q(name__contains=q_filter)|Q(desc__contains=q_filter)|Q(vendor__name__contains=q_filter))   
    if available_filter :
        products = products.filter(available=available_filter)
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
        
    qparams = {'q_filter':q_filter, 'vendor_filter': map(id_to_int, vendor_filter), 'price_from_filter':price_from_filter, 'price_to_filter':price_to_filter, 'available_filter':available_filter}
    
    qd = QueryDict(request.GET.urlencode(), mutable=True)
    try:
        qd.pop('page')
    except:
        pass
    
    try:
        qd.pop('order_by')
    except:
        pass
    
    req = {
        "products": products, 
        "direction":direction, 
        "order_by": order_by, 
        "qparams":qparams, 
        "qparams_str":qd.urlencode(), 
        "product_count":products_count,
        "vendors": vendors
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
        return page_doesnot_exist(request, num)

# product renderer
def render_product(request, product):
    return render_to_response("products/product.html", {'product':product}, get_context(request))

def get_rubrics_hierarchy_for_upload(request):
    rubrics = Rubric.objects.filter(parent__isnull=True, is_published=True).count()
    if rubrics == 0 :
        return message(request, u"Нет активных рубрик!", u"Нельзя сгенерировать прайс!")
    return rubrics_hierarchy(request, choose=True, tpl='products/construct_price.html')

def construct_price(request):
    return render("1")

# get product url
def get_product_url(product, domain):
    return xlwt.Formula(u'HYPERLINK("%s%s";"На сайте...")' % (domain, reverse('get_product', kwargs={'num':product.id})))


