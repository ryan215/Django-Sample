from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
import json
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
import datetime
from django.conf import settings
from user_auth.authentication import ExpiringTokenAuthentication
from rest_framework import exceptions

class TokenExpirationTest(APITestCase):

    def setUp(self):
        self.expires_days = getattr(settings, 'TOKEN_EXPIRE_DAYS', 14)
        self.User = User
        self.user = User.objects.create_user('bob@gmail.com', 'password')
        self.authtoken = self.user.auth_token
        self.Authentication = ExpiringTokenAuthentication()
        self.c = APIClient()


    def test_expiration_pass(self):
        """
        Using created user, expire the token then try authenticating again
        """
        user = self.user
        token = self.authtoken
        #authenticate users
        self.c.force_authenticate(user=user, token=token)


        auth_failed = False
        try:
            self.Authentication.authenticate_credentials(token)
        except exceptions.AuthenticationFailed:
            auth_failed = True
        #should pass test, within boundaries
        self.assertFalse(auth_failed)

    def test_expiration_expired(self):
        user = self.user
        token = self.authtoken
        expire_token = token.created - datetime.timedelta(days=self.expires_days, seconds=1)
        token.created = expire_token
        token.save()

        auth_failed = False
        try:
            self.Authentication.authenticate_credentials(token)
        except exceptions.AuthenticationFailed:
            auth_failed = True
        # should fail test, outside of boundaries
        self.assertTrue(auth_failed)


