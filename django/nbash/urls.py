# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns, include
from django.contrib import admin
from views import NBash
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^nbash/$', NBash.as_view()),
)
