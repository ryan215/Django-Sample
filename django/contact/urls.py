#Django Libs
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    url(r'^contact', 'contact.views.contact'),

)
