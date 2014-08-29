#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^rubrics/hierarchy/$', 'products.views.rubrics_hierarchy', name='rubrics_hierarchy'),
    url(r'^product(?P<num>[0-9]+)/$', 'products.views.get_product', name='get_product'),
)