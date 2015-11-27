import django_filters
from django.utils.timezone import utc, now
from rest_framework import filters
from rest_framework import generics
from messages.models import Message

class InboxOwnerBackendFilter(filters.BaseFilterBackend):
    """
        Returns all messages that were received by the given user and are not
        marked as deleted.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(recipient=request.user,  recipient_deleted_at__isnull=True,
        )

    class Meta:
        model = Message


class SentOwnerBackendFilter(filters.BaseFilterBackend):
    """
    Returns all messages that were sent by the given user and are not
    marked as deleted.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(
            sender=request.user,
            sender_deleted_at__isnull=True,
        )

    class Meta:
        model = Message


class DeletedOwnerBackendFilter(filters.BaseFilterBackend):
    """
    Returns all messages that were either received or sent by the given
    user and are marked as deleted.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(
            recipient=request.user,
            recipient_deleted_at__isnull=False,
        ) | queryset.filter(
            sender=request.user,
            sender_deleted_at__isnull=False,
        )
    class Meta:
        model = Message
