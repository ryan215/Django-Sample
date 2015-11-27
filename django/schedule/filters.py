import django_filters
from django.utils.timezone import utc, now
from rest_framework import filters
from rest_framework import generics
from schedule.models import Event


class EventFilter(django_filters.FilterSet):
    # start = django_filters.NumberFilter(name="price", lookup_type='gte')
    #end = django_filters.NumberFilter(name="price", lookup_type='lte')

    class Meta:
        model = Event
        fields = ['start', ]


class DatetimeFilterBackend(filters.BaseFilterBackend):
    """
    Giving month or year in query parameters allows to filter
    by either or
    """

    def filter_queryset(self, request, queryset, view):
        if 'month' in request.QUERY_PARAMS:
            month = request.QUERY_PARAMS['month']
            try:
                queryset = queryset.filter(start__month=month)
            except:
                pass

        if 'year' in request.QUERY_PARAMS:
            year = request.QUERY_PARAMS['year']
            try:
                queryset = queryset.filter(start__year=year)
            except:
                pass

        return queryset

    class Meta:
        model = Event


class NowFilterBackend(filters.BaseFilterBackend):
    """
    Filters by the current month/year
    """

    def filter_queryset(self, request, queryset, view):
        now_time = now()
        queryset = queryset.filter(start__year=now_time.year, start__month=now_time.month)
        return queryset

        return queryset

    class Meta:
        model = Event

