#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^upload_entity/$', 'entities.views.upload_entity', name='upload_entity'),
    url(r'^do_upload_entity/$', 'entities.views.do_upload_entity', name='do_upload_entity'),
)
