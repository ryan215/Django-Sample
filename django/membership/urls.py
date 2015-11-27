#Django Libs
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    url(r'^auth', 'membership.views.upgrade'),
    url(r'^upgrade-tier', 'membership.views.user_tier'),
    url(r'^upgrade-pro', 'membership.views.upgrade_to_professional'),
    url(r'^cancel', 'membership.views.cancel'),

)
