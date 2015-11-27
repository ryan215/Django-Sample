"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test import Client
from user_app.models import LefUser, Professional

class SimpleTest(TestCase):
    def setUp(self):
        self.user = LefUser(email='user@test.com', password='test')
        self.professional = Professional(email='professional@test.com', password='test')


    def test_shopify_create(self):
        print self.user
        print self.professional
        #self.assertEqual()

    def test_another_test(self):
        pass

    def test_details(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
