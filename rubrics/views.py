#-*- coding: utf-8 -*-

from django.shortcuts import render
from rubrics.models import Rubric
from utils.views import get_context
from django.shortcuts import redirect, render_to_response, render

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
    parents_id = get_parents_id(rubric, [])
    return render_to_response("rubrics/rubrics.html", {'main': rubric, 'rubrics':rubrics, 'parents_id':parents_id}, get_context(request))
