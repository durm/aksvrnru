#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^rubrics/hierarchy/$', 'products.views.rubrics_hierarchy', name='rubrics_hierarchy'),
    url(r'^login_page/$', 'products.views.login_page', name='login_page'),
    url(r'^login/$', 'products.views.login_proc', name='login'),
    url(r'^me/$', 'products.views.me', name='me'),
)
