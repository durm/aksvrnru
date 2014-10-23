#-*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, RequestContext
from aksvrnru.views import error
from pages.models import PagesSettings

def get_context(request):
    try:
        pages_settings = PagesSettings.objects.all()[0]
    except:
        pages_settings = None

    return RequestContext(request, {'pages_settings':pages_settings})
