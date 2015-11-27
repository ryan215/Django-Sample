#Django Libs
from django import forms
#Rest Libs
from rest_framework import serializers
#Models
from django.contrib.auth import get_user_model
User = get_user_model()


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(widget=forms.PasswordInput())


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'tier')

