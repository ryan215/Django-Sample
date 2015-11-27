from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView

from taggit.models import TaggedItem, Tag

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics

from taggit.serializers import TagSerializer

def tagged_object_list(request, slug, queryset, **kwargs):
    if callable(queryset):
        queryset = queryset()
    tag = get_object_or_404(Tag, slug=slug)
    qs = queryset.filter(pk__in=TaggedItem.objects.filter(
        tag=tag, content_type=ContentType.objects.get_for_model(queryset.model)
    ).values_list("object_id", flat=True))
    if "extra_context" not in kwargs:
        kwargs["extra_context"] = {}
    kwargs["extra_context"]["tag"] = tag
    return ListView.as_view(request, qs, **kwargs)


class TagViewSet(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    model = Tag
    serializer = TagSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )