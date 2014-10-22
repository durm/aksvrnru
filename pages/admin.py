#-*- coding: utf-8 -*-

from django.contrib import admin
from pages.models import Page, PagesSettings

admin.site.register(Page)
admin.site.register(PagesSettings)
