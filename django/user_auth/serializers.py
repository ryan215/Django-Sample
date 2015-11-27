#Django Libs
from django import forms
#DRF Libs
from rest_framework.authtoken.models import Token
from rest_framework import serializers
#Models
from user_app.models import Professional
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
User = get_user_model()



class CreateUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'password2', 'gender', 'tier')
        write_only_fields = ('password', )

    def validate_password(self, attrs, source):
        password = attrs['password']
        password_length = 8
        if len(password) < password_length:
          raise serializers.ValidationError('Password must be at least ' + str(password_length) + ' characters')
        return attrs

    def validate_password2(self, attrs, source):
        password2 = attrs.pop(source)
        if attrs['password'] != password2:
            raise serializers.ValidationError('Both passwords must match')
        return attrs

    def to_native(self, obj):
        self.fields.pop('password2')
        return super(CreateUserSerializer, self).to_native(obj)

    def restore_object(self, attrs, instance=None):
        tags = attrs.pop('password2', None)
        obj = super(CreateUserSerializer, self).restore_object(attrs, instance)
        return obj


class CreateProSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        widget=forms.PasswordInput(),
        required=False
    )


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ReturnUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'id')


class LogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email',)

    def restore_object(self, attrs, instance=None):
        email = attrs.pop('email', None)
        #obj = super(LogoutSerializer, self).restore_object(attrs, instance)
        obj = User.objects.get(email=email)
        return obj


class ChangePasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    current_password = serializers.CharField(
        widget=forms.PasswordInput(),
        required=False
    )
    password = serializers.CharField(
        widget=forms.PasswordInput(),
        required=False
    )
    password2 = serializers.CharField(
        widget=forms.PasswordInput(),
        required=False
    )

    def validate_token(self, attrs, source):
        token = attrs[source]
        token_array = Token.objects.filter(key = token)
        if token_array:
            return attrs
        else:
            raise serializers.ValidationError('User does not exist')

    def validate_password(self, attrs, source):
        password = attrs['password']
        password_length = 8
        if len(password) < password_length:
          raise serializers.ValidationError('Password must be at least ' + str(password_length) + ' characters')
        return attrs

    def validate_password2(self, attrs, source):
        password2 = attrs.pop(source)
        if attrs['password'] != password2:
            raise serializers.ValidationError('Both passwords must match')
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, attrs, source):
        email = attrs[source]
        user_array = User.objects.filter(email = email)
        if user_array:
            return attrs
        else:
            raise serializers.ValidationError('User does not exist')


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    change_password_token = serializers.CharField(
        widget=forms.PasswordInput(),
        required=False
    )
    password = serializers.CharField(
        widget=forms.PasswordInput(),
        required=False
    )
    password2 = serializers.CharField(
        widget=forms.PasswordInput(),
        required=False
    )

    def validate_email(self, attrs, source):
        email = attrs[source]
        user_array = User.objects.filter(email = email)
        if user_array:
            return attrs
        else:
            raise serializers.ValidationError('User does not exist')

    def validate_password(self, attrs, source):
        password = attrs['password']
        password_length = 8
        if len(password) < password_length:
          raise serializers.ValidationError('Password must be at least ' + str(password_length) + ' characters')
        return attrs

    def validate_password2(self, attrs, source):
        password2 = attrs.pop(source)
        if attrs['password'] != password2:
            raise serializers.ValidationError('Both passwords must match')
        return attrs

