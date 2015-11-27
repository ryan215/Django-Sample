# -*- coding: utf-8 -*-
"""
tests.users.test_views
~~~~~~~~~~~~~~~~~~~~~~~

This module implements view tests which can be seen as "smoke tests"
considering they go through the whole application stack for the users
API end-points.

"""
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
import json
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

class RegistrationTokenEndpointTest(APITestCase):

    def setUp(self):
        self.User = User
        self.user = User.objects.create_user('Bob@gmail.com', 'password')
        self.c = APIClient()


    def test_registration_password_mismatch(self):
        """
        Check to see end point denies mismatch passwords

        """

        data = {'email': 'user@test.com', 'password': 'password',
                'password2':'pass'}
        response = self.c.post('/accounts/register/', data, format='json')

        self.assertEqual(response.data['password2'][0], 'Both passwords must match')
        self.assertEqual(response.status_code, 400, "User shouldn't have registered")

    def test_registration_password_short(self):
        """
        Submit a short password, expect to be denied
        """
        data = {'email': 'user@test.com', 'password': 'pass',
                'password2':'pass'}
        response = self.c.post('/accounts/register/', data, format='json')


        self.assertEqual(response.data['password'][0], 'Password must be at least 8 characters')
        self.assertEqual(response.status_code, 400)

    def test_registration_bad_email(self):
        """
        Submit a bad email
        """
        data = {'email': 'user@testm', 'password': 'password',
                'password2':'password'}
        response = self.c.post('/accounts/register/', data, format='json')

        self.assertEqual(response.data['email'][0], 'Enter a valid email address.')
        self.assertEqual(response.status_code, 400, "")

    def test_registration_pass_repeat_login(self):
        """
        Submit valid request to create user
        Resubmit same request and get "email address already exists"
        Sign in with proper credentials
        Log out
        Reattempt access a page with same credentials
        """

        # scenario 3
        data = {'email': 'user@test.com', 'password': 'password',
                'password2':'password'}

        response = self.c.post('/accounts/register/', data, format='json')
        user_data = response.data

        assert 'token' in response.data
        assert 'id' in response.data
        self.assertEqual(response.status_code, 201, "User couldn't be created")

        # scenario 3
        data = {'email': 'user@test.com', 'password': 'password',
                'password2':'password'}
        response = self.c.post('/accounts/register/', data, format='json')
        self.assertEqual(response.data['email'][0], 'User with this Email address already exists.')
        self.assertEqual(response.status_code, 400, "")

        data = {'email': 'user@test.com', 'password': 'password',
                'password2':'password'}

        response = self.c.post("/accounts/login/", data, format='json')
        self.assertEqual(response.status_code, 200, "")
        self.c.credentials(HTTP_AUTHORIZATION='Token ' + str(response.data['token']))
        response = self.c.post("/accounts/logout/", data)
        self.assertEqual(response.status_code, 200, "Submit valid request to logout user")

        response = self.c.post("/accounts/logout/", data)
        self.assertEqual(response.status_code, 401, "Submit valid request to logout user")


    def test_registration_denied(self):
        """
        Sign in without any registering
        """
        data = {'email': 'user@test.com', 'password': 'password',
                'password2':'password'}

        response = self.c.post("/accounts/login/", data, format='json')
        self.assertEqual(response.data['non_field_errors'][0], "Unable to login with provided credentials.")
        self.assertEqual(response.status_code, 400, "User couldn't be created")


