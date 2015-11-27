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
        self.user = User.objects.create_user('bob@gmail.com', '12345678')
        self.client = APIClient()


    def test_no_email(self):
        data = {'email':'', 'change_password_token':'123456', 'password':'asdfghjkl', 'password2':'asdfghjkl'}

        response = self.client.post('/accounts/reset-password/', data, format='json')
        print '1.Response:' + str(response)
        print '2.Response Code:' + str(response.status_code)

        self.assertEqual(response.data['email'][0],'This field is required.')
        self.assertEqual(response.status_code,400)


    def test_invalid_email(self):
        data = {'email':'invalid_email', 'change_password_token':'123456', 'password':'asdfghjkl', 'password2':'asdfghjkl'}

        response = self.client.post('/accounts/reset-password/', data, format='json')
        print '1.Response:' + str(response)
        print '2.Response Code:' + str(response.status_code)

        self.assertEqual(response.data['email'][0],'Enter a valid email address.')
        self.assertEqual(response.status_code,400)


    def test_new_password_to_short(self):
        data = {'email':'bob@gmail.com', 'change_password_token':'12345678', 'password':'asdfghj', 'password2':'asdfghj'}

        response = self.client.post('/accounts/reset-password/', data, format='json')
        print '1.Response:' + str(response)
        print '2.Response Code:' + str(response.status_code)

        self.assertEqual(response.data['password'][0],'Password must be at least 8 characters')
        self.assertEqual(response.status_code,400)


    def test_passwords_do_not_match(self):
        data = {'email':'bob@gmail.com', 'change_password_token':'12345678', 'password':'asdfghj89', 'password2':'asdfghjkl'}

        response = self.client.post('/accounts/reset-password/', data, format='json')
        print '1.Response:' + str(response)
        print '2.Response Code:' + str(response.status_code)

        self.assertEqual(response.data['password2'][0],'Both passwords must match')
        self.assertEqual(response.status_code,400)


    def test_invalid_change_password_token(self):
        data = {'email':'bob@gmail.com', 'change_password_token':'123456', 'password':'asdfghjkl', 'password2':'asdfghjkl'}

        response = self.client.post('/accounts/reset-password/', data, format='json')
        print '1.Response:' + str(response)
        print '2.Response Code:' + str(response.status_code)

        self.assertEqual(response.data['change_password_token'][0],'Invalid change password token')
        self.assertEqual(response.status_code,400)


    def test_success_reset_passwod(self):
        data = {'email':'bob@gmail.com', 'change_password_token':'12345678', 'password':'asdfghjkl', 'password2':'asdfghjkl'}

        response = self.client.post('/accounts/reset-password/', data, format='json')
        print '1.Response:' + str(response)
        print '2.Response Code:' + str(response.status_code)

        self.assertEqual(response.data['details'][0],'Success password changed')
        self.assertEqual(response.status_code,200)


