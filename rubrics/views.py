#-*- coding: utf-8 -*-

from django.shortcuts import render
from rubrics.models import Rubric
from products.models import Product
from utils.views import get_context
from django.shortcuts import redirect, render_to_response, render
from django.db.models import Q
import types
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def get_parents_id(rubric, ids):
    if rubric is None : return ids
    return get_parents_id(rubric.parent, ids + [rubric.id])

def rubricator(request):
    rubric_id = request.GET.get("rubric", None)
    rubric = None
    rubrics = Rubric.get_published_rubrics().filter(parent=None)
    if rubric_id is not None :
        try:
            rubric = Rubric.objects.get(id=rubric_id)
        except Rubric.DoesNotExist :
            return error(request, u"Нет рубрики с таким идентификатором!", u"")
    rubricator_path = []
    parents_id = []
    rubrics_view = rubrics
    products = Product.get_published_products()
    products_count = products.count()
    if rubric is not None :
        rubricator_path = rubric.rubricator_path()
        parents_id = map(lambda r: r.id, rubricator_path)
        all_children = rubric.get_all_published_children()
        products = products.filter(Q(rubrics__in=all_children)|Q(rubrics__in=[rubric]))
        rubrics_view = all_children
        if len(rubrics_view) :
            products = products.order_by("?")[:21]
        else:
            products_count = products.count()
            paginator = Paginator(products, 21)
            
            page = request.GET.get('page')
            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)
    
    return render_to_response("rubrics/rubrics.html", {'main': rubric, 'products':products, 'products_count':products_count, 'rubrics_view':rubrics_view, 'rubrics':rubrics, 'parents_id':parents_id, 'rubricator_path':rubricator_path}, get_context(request))
