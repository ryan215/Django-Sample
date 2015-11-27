from django.conf.urls import patterns, include, url
from rest_framework import routers

from .views import TagViewSet

router = routers.SimpleRouter(trailing_slash=False)


urlpatterns = patterns('',
    url(r'^$', TagViewSet.as_view()),

)
