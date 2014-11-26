#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^page(?P<num>[0-9]+)/$', 'pages.views.get_page', name="get_page"),
    url(r'^home/$', 'pages.views.home', name="home"),
)
