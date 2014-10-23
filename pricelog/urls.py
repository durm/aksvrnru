#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^upload_price/$', 'pricelog.views.upload_price', name='upload_price'),
    url(r'^do_upload_price/$', 'pricelog.views.do_upload_price', name='do_upload_price'),
)
