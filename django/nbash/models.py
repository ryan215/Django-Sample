# -*- coding: utf-8 -*-
from django.db import models
from provider.oauth2.models import Client, AccessToken, RefreshToken
from provider.utils import long_token


class NBash(models.Model):
    mac_id = models.CharField(max_length=50, primary_key=True)
    access_token = models.CharField(max_length=255, default=long_token)
    online = models.BooleanField(default=False)
