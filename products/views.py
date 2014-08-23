#-*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response
from products.models import Rubric

def rubrics_hierarchy(request):
    rubrics = Rubric.objects.filter(parent__isnull=True)
    return render_to_response('hierarchy/rubric_roots.html', {"rubrics":rubrics})
