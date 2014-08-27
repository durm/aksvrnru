#-*- coding: utf-8 -*-

from django.shortcuts import redirect, render_to_response
from products.models import Rubric
from pages.views import get_context
from django.contrib.auth import authenticate
from aksvrnru.views import error
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login

def rubrics_hierarchy(request):
    rubrics = Rubric.objects.filter(parent__isnull=True)
    return render_to_response('hierarchy/hierarchy.html', {"rubrics":rubrics}, get_context(request))
