
import os, sys, json, ast
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_server.settings")
from django.contrib.auth import get_user_model
User = get_user_model()
import datetime
from django.utils.timezone import utc, now
import string
#from schedule.models import Calendar, Event
#Write code after this
##############################################

from user_app.models import Professional

def create_professional_dummy_data():
    accepting = True
    tags = ["looksy", 'crossfit', 'fitness']
    profession_list = ['Nutritionist', 'Trainer']
    gender = ['M', 'F']
    counter = 0

    for letter in string.ascii_uppercase:
        email = 'pro_' + letter + '@test.com'
        password = 'admin123'
        first = 'pro_first_' + letter
        last = 'pro_last_' + letter
        pro_gender = gender[counter%2]

        data_dict = { "first_name":first, "last_name":last,
            "password":password, 'gender': pro_gender
        }
        if not Professional.objects.filter(email=email).exists():
            user = User.objects.create_user(email=email, password=password, **data_dict)
            pro = Professional.objects.create_prof(user)
            pro.is_accepting=accepting
            pro.profession = profession_list[counter%2]
            pro.tags.add(tags[counter%3])
            pro.save()
        else:
            # 'causes update with what is in the data_dict'
            # good for adding new items
            Professional.objects.filter(email=email).update(**data_dict)


        accepting = not accepting
        counter += 1


def create_user_dummy_data():
    for letter in string.ascii_uppercase:
        email = 'user_' + letter + '@test.com'
        password = 'admin123'

        first = 'user_first_' + letter
        last = 'user_last_' + letter
        if not User.objects.filter(email=email).exists():
            data_dict = {"email":email, "password" : password, "first_name":first, "last_name":last,
                "password":password,
            }
            user = User.objects.create_user(**data_dict)



