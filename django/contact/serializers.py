from rest_framework import serializers


class ContactSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()
    message = serializers.CharField()
