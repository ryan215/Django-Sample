#Django Libs
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf import settings



TOKEN_EXPIRE = getattr(settings, 'TOKEN_EXPIRE', False)
if TOKEN_EXPIRE:
    login_function = 'user_auth.views.obtain_expiring_auth_token'
else:
    login_function = 'user_auth.views.obtain_auth_token'


urlpatterns = patterns('',

    url(r'^register/?$', 'user_auth.views.register'),
    url(r'^register-professional/?$', 'user_auth.views.register_professional'),
    url(r'^login', login_function),
    url(r'^logout', 'user_auth.views.logout'),
    url(r'^change-password', 'user_auth.views.change_password'),
    url(r'^forgot-password', 'user_auth.views.forgot_password'),
    url(r'^reset-password', 'user_auth.views.reset_password'),

)
