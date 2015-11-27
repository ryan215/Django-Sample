
import os, sys, json, ast
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_server.settings")
from django.contrib.auth import get_user_model
User = get_user_model()
import datetime
from django.utils.timezone import utc, now
#from schedule.models import Calendar, Event
#Write code after this
##############################################


from feed.models import Entry, TextEntry, PhotoEntry

#Entry.objects.filter(tags__name__in=["delicious"])
# user = User.objects.get(email='admin@test.com')
# for entry in PhotoEntry.objects.all():
#     print entry
#      entry.tags.add('fitness')

# for entry in TextEntry.objects.all():
#     print entry
#      entry.tags.add('fitness')

# print Entry.objects.filter(tags__name__in=['fitness'])


#from schedule.models import Calendar

from shopify_app import shopify_call
users = User.objects.all()

for user in users:
    try:
        print user.email
        user.shopify_id = shopify_call.requests_search(user.email)['id']
        user.save()
        print user.shopify_id
    except:
        print 'doesnt exists'
