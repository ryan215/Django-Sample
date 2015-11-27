from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

class UserAuthBackend(object):
    def authenticate(self, token=None):
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
