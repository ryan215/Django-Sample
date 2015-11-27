from rest_framework import serializers
from django.utils.timezone import now
from messages.models import Message

from user_app.models import Professional
from django.contrib.auth import get_user_model
User = get_user_model()


class senderReceiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'img')


class InboxSerializer(serializers.ModelSerializer):
    sender = senderReceiverSerializer(read_only=True)
    recipient = senderReceiverSerializer(read_only=True)

    class Meta:
        model = Message

    def to_native(self, value):
        obj = super(InboxSerializer, self).to_native(value)
        return obj

class SentSerializer(InboxSerializer):
    pass
class TrashSerializer(InboxSerializer):
    pass

class DeleteSerializer(serializers.ModelSerializer):
    view = serializers.CharField(required=True)
    class Meta:
        model = Message
        fields = ('id', 'view',)
        exclude = ('img', 'body', 'subject')

    def restore_object(self, attrs, instance=None):
        """
        Given a dictionary of deserialized field values, either update
        an existing model instance, or create a new model instance.
        """
        obj = super(DeleteSerializer, self).restore_object(attrs, instance)

        if 'inbox' in attrs['view']:
            obj.recipient_deleted_at = now()
            obj.save()
        if 'sent' in attrs['view']:
            obj.sender_deleted_at = now()
            obj.save()

        return obj


class UnDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id',)


    def restore_object(self, attrs, instance=None):
        """
        Given a dictionary of deserialized field values, either update
        an existing model instance, or create a new model instance.
        """
        obj = super(UnDeleteSerializer, self).restore_object(attrs, instance)

        obj.recipient_deleted_at = None
        obj.save()
        return obj


class ComposeSerializer(serializers.ModelSerializer):
    # recipient = serializers.SlugRelatedField(slug_field="email")

    class Meta:
        model = Message
        fields = ('recipient', 'subject', 'body', 'sender')

    def __init__(self, *args, **kwargs):

        # Logged in user to be sender
        try:
            user = kwargs['context']['request'].user
            kwargs['data']['sender'] = user.pk
        except:
            pass
        return super(ComposeSerializer, self).__init__(*args, **kwargs)


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        #fields = ('id',)

    def restore_object(self, attrs, instance=None):
        """
        Given a dictionary of deserialized field values, either update
        an existing model instance, or create a new model instance.
        """
        obj = super(ReplySerializer, self).restore_object(attrs, instance)
        return obj

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'img',)

class ProfessionalConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = ('id', 'first_name', 'last_name', 'img',)

class ConnectionSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(max_length=50, required=False)
    connection = ProfessionalConnectionSerializer(required=False)

    class Meta:
        model = User
        fields = ('id', 'connection', 'user_id')


    def to_native(self, value):
        #print value
        obj = super(ConnectionSerializer, self).to_native(value)

        is_professional = Professional.objects.filter(id=value.id).exists()
        user_id = obj.get('user_id')
        user = None
        if User.objects.filter(pk=user_id).exists():
            user = User.objects.get(pk=user_id)

        #if professional, all connections allowed
        if is_professional and user:
            obj['connection'] = AdminSerializer(instance=user).data
        elif user:
        # if admin, then allow connection to be made
            if user.is_staff:
                obj['connection'] = AdminSerializer(instance=user).data
        return obj


