#-*- coding: utf-8 -*-

from django.contrib import admin
from pages.models import *

admin.site.register(Page)
admin.site.register(PagesSettings)

# Register your models here.
