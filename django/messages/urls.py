from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from django.conf.urls import patterns, include, url
from rest_framework import routers

from messages.views import InboxListView, SentListView, ComposeMessageObjView
from messages.views import DeletedListView, DeleteMessageObjView, UnDeleteMessageObjView
from messages.views import ReplyMessageObjView, ConnectionView, MessageView


# urlpatterns = patterns('',
#     url(r'^$', RedirectView.as_view(url='inbox/'), name='messages_redirect'),

#     url(r'^compose/$', compose, name='messages_compose'),
#     url(r'^compose/(?P<recipient>[\w.@+-]+)/$', compose, name='messages_compose_to'),
#     url(r'^reply/(?P<message_id>[\d]+)/$', reply, name='messages_reply'),

# )

#COMPLETED
#     url(r'^inbox/$', inbox, name='messages_inbox'),
#     url(r'^outbox/$', outbox, name='messages_outbox'),
#     url(r'^delete/(?P<message_id>[\d]+)/$', delete, name='messages_delete'),
#     url(r'^undelete/(?P<message_id>[\d]+)/$', undelete, name='messages_undelete'),
#     url(r'^trash/$', trash, name='messages_trash'),

router = routers.SimpleRouter(trailing_slash=False)


urlpatterns = patterns('',
    url(r'^inbox$', InboxListView.as_view()),
    url(r'^sent$', SentListView.as_view()),
    url(r'^trash$', DeletedListView.as_view()),
    url(r'^compose$', ComposeMessageObjView.as_view()),
    url(r'^connection/(?P<pk>[0-9]+)$', ConnectionView.as_view()),
    url(r'^reply/(?P<message_id>[\d]+)$', ReplyMessageObjView.as_view()),
    url(r'^delete/(?P<pk>[0-9]+)$', DeleteMessageObjView.as_view()),
    url(r'^undelete/(?P<pk>[0-9]+)$', UnDeleteMessageObjView.as_view()),
     url(r'^message/(?P<pk>[0-9]+)$', MessageView.as_view()),

)
