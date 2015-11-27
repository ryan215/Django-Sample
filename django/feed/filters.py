import django_filters
from django.utils.timezone import utc, now
from rest_framework import filters
from rest_framework import generics
from feed.models import Entry, TextEntry, PhotoEntry, VideoEntry, EventEntry, BlogEntry

class TypeFilterBackend(filters.BaseFilterBackend):
    """
    Giving month or year in query parameters allows to filter
    by either or
    """
    def filter_queryset(self, request, queryset, view):
        if 'type' in request.QUERY_PARAMS:
            obj_type = request.QUERY_PARAMS['type']
            queryset = queryset.filter(type=obj_type)

        return queryset
