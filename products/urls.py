#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^rubrics/hierarchy/$', 'products.views.rubrics_hierarchy', name='rubrics_hierarchy'),
)
