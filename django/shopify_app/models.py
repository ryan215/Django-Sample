from django.db import models

class ShopifySessionManager(models.Manager):

    def get_session(self):
        try:
            return super(ShopifySessionManager, self).get(pk=1)
        except:
            return ShopifySession().save()


# Create your models here.
class ShopifySession(models.Model):
    shop_url = models.CharField(max_length=50, blank=True)
    access_token = models.CharField(max_length=50, blank=True)
    objects = ShopifySessionManager()

    def __unicode__(self):
        return self.access_token

    def set_session(self, url, token):
        self.shop_url = url
        self.access_token = token
        self.save()
