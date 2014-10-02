#-*- coding: utf-8 -*-

from django.shortcuts import redirect, render_to_response, render
from products.models import Rubric, Price, Product, Vendor, sale_rate
from pages.views import get_context
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
from products.tasks import proc

def rubrics_hierarchy(request, choose=False, tpl='hierarchy/hierarchy.html', is_published=True):
    rubrics = Rubric.objects.filter(parent__isnull=True, is_published=True)
    if rubrics.count() :
        return render_to_response(tpl, {"rubrics":rubrics, "choose":choose, "sale_rate": sale_rate}, get_context(request))
    else:
        return message(request, u"Нет активных рубрик!", u"")

def upload_price(request):
    if request.user.is_authenticated() and request.user.is_staff :
        return render_to_response("products/upload_price.html", {}, get_context(request))
    else:
        return error(request, u"Ошибка доступа", u"Только персонал может загрузить и распарсить прайс!")

def do_upload_price(request):
    if request.user.is_authenticated() and request.user.is_staff :
        f = request.FILES['price']
        price = Price.objects.create(name="%s.xsl"%(uuid.uuid4()), file=f)
        price.save()
        
        proc.delay(request.user.id, price.id)
        
        return message(request, u"В обработке!", u"Прайс парсится")
    else:
        return error(request, u"Ошибка доступа", u"Только персонал может загрузить и распарсить прайс!")

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
        return message(request, "Нет активных рубрик!", "Нельзя сгенерировать прайс!")
    return rubrics_hierarchy(request, choose=True, tpl='hierarchy/construct_price.html')

def construct_price(request):
    
    price_type = request.POST.get("price_type", "retail")
    sale = request.POST.get("sale", None)
    
    if sale is not None :
        sale = float(sale.replace(",","."))
        
    rubrics_ids = request.POST.getlist("rubric")

    if price_type is None or len(rubrics_ids) == 0 :
        return error(request, "Ошибка", "Не задан тип прайса или не выбраны рубрики")

    wb = xlwt.Workbook()
    ws = wb.add_sheet('Page1')

    rubrics = Rubric.objects.filter(parent__isnull=True, is_published=True, id__in=rubrics_ids)

    price_desc = u" для розницы " if price_type == "retail" else u" для розницы опта "

    style_string = "borders: top medium, bottom medium, left medium, right medium"
    style = xlwt.easyxf(style_string)

    product_style_string = "borders: bottom thin, left thin, right thin"
    product_style = xlwt.easyxf(style_string)

    ws.write(0, 0, u"Прайс%sсгенерирован %s" % (price_desc, str(datetime.now())))
    ws.write(1, 0, u"Наименование товара", style)
    ws.write(1, 1, u"Цена", style)
    ws.write(1, 2, u"Ссылка", style)

    col = ws.col(0)
    col.width = 1200 * 20

    r = 1
    for rubric in rubrics :
        r = write_rubric(ws, r, rubric, get_root_rubric_style(), filt=rubrics_ids, product_style=product_style, sale=sale, price_type=price_type)

    f = StringIO.StringIO()

    wb.save(f)

    response = HttpResponse(f.getvalue(), content_type="application/vnd.ms-excel")
    response['Content-Disposition'] = 'attachment; filename=price_%s.xls' % str(uuid.uuid4())
    return response

def write_rubric(ws, r, rubric, style=xlwt.XFStyle(), filt=None, product_style=None, sale=None, price_type="retail"):
    r += 1
    ws.write(r, 0, rubric.name, style)
    ws.write(r, 1, "", style)
    ws.write(r, 2, "", style)
    for product in rubric.get_published_products() :
        r = write_product(ws, r, product, style=product_style, sale=sale, price_type=price_type)
    childs = rubric.get_published_children()
    if filt is not None :
        childs = childs.filter(id__in=filt)
    for child in childs :
        r = write_rubric(ws, r, child, get_rubric_stile(), filt=filt, product_style=product_style, sale=sale, price_type=price_type)
    return r

def get_product_price_by_type_with_sale(product, price_type, sale=None):
    if product.by_order :
        return u"Под заказ"
    if product.is_recommend_price :
        return product.retail_price
    if not product.available :
        return u"--"
    if sale is None :
        return product.retail_price_with_sale()
    else:
        return product.retail_price_with_sale(s=sale)
    
def write_product(ws, r, product, style=None, sale=None, price_type="retail"):
    r += 1
    ws.write(r, 0, "%s | %s | %s" % (product.vendor.name, product.name, product.short_desc), style)
    
    price = get_product_price_by_type_with_sale(product, price_type, sale)
    
    ws.write(r, 1, price, style)
    ws.write(r, 2, xlwt.Formula(u'HYPERLINK("%s%s";"На сайте...")' % (settings.DOMAIN_, reverse('get_product', kwargs={'num':product.id}))), style)
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
