#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^rubricator/$', 'rubrics.views.rubricator', name='rubricator'),
    #
    url(r'^rubricator/create/$', 'rubrics.views.create_rubricator_from_file', name='create_rubricator_from_file'),
    url(r'^rubricator/create/do/$', 'rubrics.views.do_create_rubricator_from_file', name='do_create_rubricator_from_file'),
)
