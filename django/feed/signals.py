import datetime
from django.contrib.auth import get_user_model
User = get_user_model()
#from models import Event, Calendar
from models import Event
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.utils.timezone import utc, now

# @receiver(post_save, sender=User)
# def create_user_calendar(sender, instance=None, created=False, **kwargs):
#     """
#     Creates a calendar per user, and attaches an event saying when user
#     created profile
#     """
#     if created:
#                 obj, created = Calendar.objects.get_or_create(user=instance)
#                 user = instance
#                 title = 'Account created'
#                 description = 'Account was created!'
#                 start = now()
#                 end = now() + datetime.timedelta(hours=1)
#                 data = {'creator' : user,
#                         'title' : title,
#                         'description' : description,
#                         'start' : start,
#                         'end' : end,
#                         'calendar' : obj
#                         }
#                 create_event = Event(**data)

#                 create_event.save()

#                 #print obj, created




