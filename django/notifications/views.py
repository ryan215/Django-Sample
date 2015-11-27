# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render, redirect
from django.template.context import RequestContext
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.response import Response

from .models import Notification
from .permissions import IsAdminOrSelf
from .serializers import AllNotificationSerializer


class AllNotificationViewSet(viewsets.ModelViewSet):
    model = Notification
    serializer_class = AllNotificationSerializer
    permission_classes = (IsAdminOrSelf,)

    def get_queryset(self):
        return self.request.user.notifications.filter(unread = True)

    def update(self, request, pk=None):
        if Notification.objects.filter(pk = pk).exists():
            notification =  Notification.objects.get(pk = pk)
            notification.unread = False
            notification.save()
        else:
            pass
        return Response({'details':['success']}, status=status.HTTP_200_OK)

