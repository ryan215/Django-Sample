import datetime
import os

from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()
#from schedule.models import Event, Calendar
from schedule.models import Event

class TestEvent(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('bob@gmail.com', 'password')
        # self.recurring_data = {
        #         'title': 'Recent Event',
        #         'start': datetime.datetime(2008, 1, 5, 8, 0),
        #         'end': datetime.datetime(2008, 1, 5, 9, 0),
        #         'end_recurring_period' : datetime.datetime(2008, 5, 5, 0, 0),
        #         #'calendar': cal
        #        }
        # self.data = {
        #         'title': 'Recent Event',
        #         'start': datetime.datetime(2008, 1, 5, 8, 0),
        #         'end': datetime.datetime(2008, 1, 5, 9, 0),
        #         'end_recurring_period' : datetime.datetime(2008, 5, 5, 0, 0),
        #         #'calendar': cal
        #        }

#    def test_calendar(self):
#        print 'dib'
#        print self.user.calendar
#        self.assertFalse(True)
