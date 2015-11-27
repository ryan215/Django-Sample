from django.conf.urls import patterns, include, url
from django.conf import settings
from rest_framework import routers
from feed.views import PhotoEntryViewSet, VideoEntryViewSet, BlogEntryViewSet, EntryListView, TextEntryViewSet, EventEntryViewSet
from feed.views import CommentViewSet, FlaggedCreateView, EntryLikeView, ListSubEntryView, SharedEntryViewSet, ClientListView, ClientFilterView
from feed.views import RelationshipTypeAheadView, EntryView, GroupEntryView

router = routers.SimpleRouter(trailing_slash=False)
router.register('/text', TextEntryViewSet)
router.register('/photo', PhotoEntryViewSet)
router.register('/video', VideoEntryViewSet)
router.register('/event', EventEntryViewSet)
router.register('/blog', BlogEntryViewSet)
router.register('/shared', SharedEntryViewSet)
router.register('/comment', CommentViewSet)



urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^$', EntryListView.as_view()),
    url(r'^/entry/(?P<pk>[0-9]+)$', EntryView.as_view()),
    url(r'^/(?P<pk>[0-9]+)$', EntryListView.as_view()),
    url(r'^/likes/(?P<pk>[0-9]+)$', EntryLikeView.as_view()),
    url(r'^/flag$', FlaggedCreateView.as_view()),
    url(r'^/(?P<type>[a-z]+)/list/(?P<pk>[0-9]+)', ListSubEntryView.as_view()),
    url(r'^/group/(?P<tag_name>[-\w]+)$', GroupEntryView.as_view()),
    url(r'^/group/(?P<tag_name>[-\w]+)/(?P<type>[a-z]+)', GroupEntryView.as_view()),
    url(r'^/client$', ClientListView.as_view()),
    #url(r'^/client/(?P<pk>[0-9]+)$', ClientListView.as_view()),
    url(r'^/client/(?P<type>[a-z]+)/', ClientFilterView.as_view()),
    url(r'^/typeahead?$', RelationshipTypeAheadView.as_view()),
)
