from django import forms
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import serializers
from .models import Notification



class AllNotificationSerializer(serializers.ModelSerializer):
    message = serializers.Field(source="message")
    target_object_id = serializers.Field(source="target_object_id")
    target_content_type = serializers.RelatedField(many=False)
    class Meta:
        model = Notification
        fields = (    "id", "level", "unread", "timestamp", "public", "message", "target_object_id", 'target_content_type')


