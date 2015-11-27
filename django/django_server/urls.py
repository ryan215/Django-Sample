from django.conf.urls import patterns, include, url
from django.conf import settings
from user_app.views import StaticTagViewSet
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users', include('user_app.urls')),
    url(r'^accounts/', include('user_auth.urls')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^all-tags', include('taggit.urls')),
    url(r'^tags', StaticTagViewSet.as_view()),
    url(r'^workouts/', include('workouts.urls')),
    url(r'^messages/', include('messages.urls')),
    url(r'^upload-image/', include('cicu.urls')),
    url(r'^contact/', include('contact.urls')),
    url(r'^membership/', include('membership.urls')),
    url(r'^calendar/', include('schedule.urls')),
    url(r'^feed', include('feed.urls')),
    url(r'^notifications', include('notifications.urls')),
)


if settings.DEBUG:
    urlpatterns = patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #static
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.STATIC_ROOT}),

    #media
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),


) + urlpatterns
