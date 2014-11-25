#-*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from aksvrnru import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^$', 'pages.views.home', name='home'),
    url(r'^products/', include('products.urls')),
    url(r'^pages/', include('pages.urls')),
    url(r'^userprofiles/', include('userprofiles.urls')),

    url(r'^pricelog/', include('pricelog.urls')),
    url(r'^rubrics/', include('rubrics.urls')),
    url(r'^previews/', include('previews.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
