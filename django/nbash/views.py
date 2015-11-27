# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
import redis
from ws4redis import settings as redis_settings
from models import NBash as Bashes



class NBash(TemplateView):
    template_name = 'nbash.html'

    def get_context_data(self, **kwargs):
        context = super(NBash, self).get_context_data(**kwargs)
        mac = self.request.GET.get("macId")
        if mac:
            context.update(nbash_url='ws://{HTTP_HOST}/ws/nbashes/'.format(**self.request.META) + mac)

        bashes = Bashes.objects.all()
        context.update(bashes=bashes, nbashes_url='ws://{HTTP_HOST}/ws/nbashes'.format(**self.request.META))
        return context

