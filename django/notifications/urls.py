from django.conf.urls import patterns, include, url
from rest_framework import routers
from .views import AllNotificationViewSet
from django.conf.urls import *


router = routers.SimpleRouter(trailing_slash=False)
router.register(r'', AllNotificationViewSet)


urlpatterns = patterns('notifications.views',

    url(r'^', include(router.urls)),
)
