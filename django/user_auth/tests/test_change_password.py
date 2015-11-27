from django.conf import settings
from django.contrib.auth.models import check_password
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
import json



class ChangePassword(APITestCase):

    def setUp(self):
        self.User = User
        self.user = User.objects.create_user('bob@gmail.com', 'password')
        self.client = APIClient()


    def test_user_does_not_exist(self):
        token = Token.objects.get(user = self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        data = {'token':'wrong_token', 'current_password':'password', 'password':'password123', 'password2':'password123'}

        response = self.client.post('/accounts/change-password/', data, format='json')
        print '1.Response:' + str(response)
        print '2.Response Code:' + str(response.status_code)

        self.assertEqual(response.data['token'][0],'User does not exist')
        self.assertEqual(response.status_code,400)


    def test_password_to_short(self):
        token = Token.objects.get(user = self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        data = {'token':token.key, 'current_password':'password', 'password':'123', 'password2':'123'}

        response = self.client.post('/accounts/change-password/', data, format='json')
        print '1.Response:' + str(response)
        print '2.Response Code:' + str(response.status_code)

        self.assertEqual(response.data['password'][0], 'Password must be at least 8 characters')
        self.assertEqual(response.status_code,400)


    def test_passwords_must_match(self):
        token = Token.objects.get(user = self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        data = {'token':token.key, 'current_password':'password', 'password':'password123', 'password2':'password'}

        response = self.client.post('/accounts/change-password/', data, format='json')
        print '1.Response:' + str(response)
        print '2.Response Code:' + str(response.status_code)

        self.assertEqual(response.data['password2'][0], 'Both passwords must match')
        self.assertEqual(response.status_code,400)


    def test_wrong_current_password(self):
        token = Token.objects.get(user = self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        data = {'token':token.key, 'current_password':'wrong_password', 'password':'password123', 'password2':'password123'}

        response = self.client.post('/accounts/change-password/', data, format='json')
        print '1.Response:' + str(response)
        print '2.Response Code:' + str(response.status_code)

        self.assertEqual(response.data['current_password'][0], 'Wrong current password')
        self.assertEqual(response.status_code,400)


    def test_success_password_change(self):
        token = Token.objects.get(user = self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        data = {'token':token.key, 'current_password':'password', 'password':'password123', 'password2':'password123'}

        response = self.client.post('/accounts/change-password/', data, format='json')
        print '1.Response:' + str(response)
        print '2.Response Code:' + str(response.status_code)

        # print check_password('password123', self.user.password)

        self.assertEqual(response.data['details'][0], 'Success password changed')
        self.assertEqual(response.status_code,200)
