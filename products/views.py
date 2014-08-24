#-*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response
from products.models import Rubric
from pages.views import get_context

def rubrics_hierarchy(request):
    rubrics = Rubric.objects.filter(parent__isnull=True)
    return render_to_response('hierarchy/hierarchy.html', {"rubrics":rubrics}, get_context(request))
