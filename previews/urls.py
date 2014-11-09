#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^upload_zip/$', 'previews.views.upload_zip', name='upload_zip'),
    url(r'^do_upload_zip/$', 'previews.views.do_upload_zip', name='do_upload_zip'),
)
