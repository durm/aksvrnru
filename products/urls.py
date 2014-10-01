#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^rubrics/hierarchy/$', 'products.views.rubrics_hierarchy', name='rubrics_hierarchy'),
    url(r'^rubrics/get_rubrics_hierarchy_for_upload/$', 'products.views.get_rubrics_hierarchy_for_upload', name='get_rubrics_hierarchy_for_upload'),
    url(r'^rubrics/construct_price/$', 'products.views.construct_price', name='construct_price'),
    url(r'^upload_price/$', 'products.views.upload_price', name='upload_price'),
    url(r'^do_upload_price/$', 'products.views.do_upload_price', name='do_upload_price'),
    url(r'^product(?P<num>[0-9]+)/$', 'products.views.get_product', name='get_product'),
    url(r'^listing/$', 'products.views.listing', name='listing'),

)
