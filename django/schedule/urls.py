from django.conf.urls import patterns, include, url
from django.conf import settings
from rest_framework import routers
from schedule.views import EventViewSet


urlpatterns = patterns('',
    url(r'^(?P<pk>[0-9]+)$', EventViewSet.as_view()),
    url(r'^$', EventViewSet.as_view()),
    # url(r'^event/(?P<pk>[0-9]+)$', EventObjectViewSet.as_view()),
)
