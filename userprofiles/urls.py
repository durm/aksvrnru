#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^login_page/$', 'userprofiles.views.login_page', name='login_page'),
    url(r'^login/$', 'userprofiles.views.login_proc', name='login'),
    url(r'^me/$', 'userprofiles.views.me', name='me'),
    url(r'^logout/$', 'userprofiles.views.logout_view', name='logout_view'),
    url(r'^signup_view/$', 'userprofiles.views.signup_view', name='signup_view'),
    url(r'^signup/$', 'userprofiles.views.signup', name='signup'),
    url(r'^edit_profile_view/$', 'userprofiles.views.edit_profile_view', name='edit_profile_view'),
    url(r'^edit_profile/$', 'userprofiles.views.edit_profile', name='edit_profile'),
    url(r'^edit_profile_passwd/$', 'userprofiles.views.edit_profile_passwd', name='edit_profile_passwd'),
    url(r'^bookcall/$', 'userprofiles.views.bookcall', name='bookcall'),
    url(r'^send_bookcall/$', 'userprofiles.views.send_bookcall', name='send_bookcall'),
    url(r'^feedback/$', 'userprofiles.views.feedback', name='feedback'),
    url(r'^send_feedback/$', 'userprofiles.views.send_feedback', name='send_feedback'),
)
