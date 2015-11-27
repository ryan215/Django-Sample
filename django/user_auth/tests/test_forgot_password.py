from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
import json
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.contrib.auth.models import check_password


class ChangePassword(APITestCase):

    def setUp(self):
        self.User = User
        self.user = User.objects.create_user('bob@gmail.com', 'password')
        self.client = APIClient()


    def test_no_email(self):
        data = {'email':''}
        response = self.client.post('/accounts/forgot-password/', data, format='json')
        print '1.Response:' + str(response)
        print '2.Response Code:' + str(response.status_code)

        self.assertEqual(response.data['email'][0],'This field is required.')
        self.assertEqual(response.status_code,400)


    def test_invalid_email(self):
        data = {'email':'invalid'}
        response = self.client.post('/accounts/forgot-password/', data, format='json')
        print '1.Response:' + str(response)
        print '2.Response Code:' + str(response.status_code)

        self.assertEqual(response.data['email'][0],'Enter a valid email address.')
        self.assertEqual(response.status_code,400)


    def test_user_does_not_exist(self):
        data = {'email':'this_user_does_not_exist@yahoo.com'}
        response = self.client.post('/accounts/forgot-password/', data, format='json')
        print '1.Response:' + str(response)
        print '2.Response Code:' + str(response.status_code)

        self.assertEqual(response.data['email'][0],'User does not exist')
        self.assertEqual(response.status_code,400)


    def test_user_does_not_exist(self):
        data = {'email':'this_user_does_not_exist@yahoo.com'}
        response = self.client.post('/accounts/forgot-password/', data, format='json')
        print '1.Response:' + str(response)
        print '2.Response Code:' + str(response.status_code)

        self.assertEqual(response.data['email'][0],'User does not exist')
        self.assertEqual(response.status_code,400)


    def test_success_email_sent(self):
        data = {'email':'bob@gmail.com'}
        response = self.client.post('/accounts/forgot-password/', data, format='json')
        print '1.Response:' + str(response)
        print '2.Response Code:' + str(response.status_code)

        self.assertEqual(response.data['details'][0],'Email sent')
        self.assertEqual(response.status_code,200)


