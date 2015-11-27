import django_filters
from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework import viewsets, status, filters
from .models import Professional


class UserFilter(django_filters.FilterSet):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'gender',]

class QueueFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(queue=False)

    class Meta:
        model = Professional


class GenderFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if 'gender' in request.QUERY_PARAMS:
            gender = request.GET.getlist('gender','')
            try:
                queryset = queryset.filter(gender__in= gender)
            except:
                pass

        return queryset

    class Meta:
        model = Professional


class ProfessionFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if 'profession' in request.QUERY_PARAMS:
            profession = request.GET.getlist('profession','')
            try:
                queryset = queryset.filter(profession__in= profession)
            except:
                pass

        return queryset

    class Meta:
        model = Professional


class LocationFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if 'location' in request.QUERY_PARAMS:
            location = request.GET.getlist('location','')
            try:
                queryset = queryset.filter(location__in= location)
            except:
                pass

        return queryset

    class Meta:
        model = Professional


class AcceptingFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if 'accepting' in request.QUERY_PARAMS:
            accepting = request.GET.get('accepting','')
            if (accepting == 'true'):
                accepting = [True]
            elif (accepting == 'false'):
                accepting = [False]
            else:
                accepting = [True, False]
            try:
                queryset = queryset.filter(is_accepting__in = accepting)
            except:
                pass

        return queryset

    class Meta:
        model = Professional


class TagFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if 'tags' in request.QUERY_PARAMS:
            tags = request.GET.getlist('tags','')
            try:
                for tag in tags:
                    special_list = [tag]
                    queryset = queryset.filter(tags__name__in=special_list)
            except:
                pass

        return queryset

    class Meta:
        model = Professional


class OwnerFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(connection=request.user)

    class Meta:
        model = User

