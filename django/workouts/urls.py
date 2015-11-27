from django.conf.urls import patterns, include, url
from django.conf import settings
from rest_framework import routers

from workouts.views import VideoListView, VideoObjectView, TitleViewSet, CommentObjView, VideoLikeView
from workouts.views import CommentListView


router = routers.SimpleRouter(trailing_slash=False)
#router.register('comments', CommentViewSet)


urlpatterns = patterns('',
    url(r'^video?$', VideoListView.as_view()),
    url(r'^video/(?P<pk>[0-9]+)$', VideoObjectView.as_view()),
    url(r'^video/comments/(?P<pk>[0-9]+)$', CommentListView.as_view()),
    url(r'^video/likes/(?P<pk>[0-9]+)$', VideoLikeView.as_view()),
    url(r'^comments/(?P<pk>[0-9]+)$', CommentObjView.as_view()),
    url(r'^titles?$', TitleViewSet.as_view()),
)
