from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
User = get_user_model()
import os
# FOR MORE INFORMATION REFER TO THIS
# https://django-model-utils.readthedocs.org/en/latest/managers.html
from model_utils.models import TimeStampedModel, TimeFramedModel
from model_utils.managers import InheritanceManager

from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

def get_upload_path(instance, filename):
    now_time = now().strftime("%m_%d_%Y_%H_%M_%S_%f_")
    return os.path.join(
          "users","%d" % instance.user.id, instance.type, now_time+filename )

class TaggedEntry(TaggedItemBase):
    content_object = models.ForeignKey('Entry')

class Entry(TimeStampedModel):
    """
    Entry class will be abstracted in order to
    define the types of entries
    """
    type = "text"
    user = models.ForeignKey(User, related_name="%(app_label)s_%(class)s")
    text = models.TextField(_('text'), max_length=500000, blank=True)
    likes = models.ManyToManyField(User, related_name='entries_liked', blank=True,null=True)
    objects = InheritanceManager()
    tags = TaggableManager(through=TaggedEntry, blank=True)
    def __unicode__(self):
        return str(self.id)

class TextEntry(Entry):
    type = 'text'

class PhotoEntry(Entry):
    type = 'photo'
    img = models.ImageField(_('image'), upload_to=get_upload_path, blank=False)

class VideoEntry(Entry):
    type = 'video'
    url = models.CharField(_('Url'), max_length=100, default='')

class BlogEntry(Entry):
    type = 'blog'
    # WARNING: When changing max_length refer to
    # http://stackoverflow.com/questions/2108824/mysql-incorrect-string-value-error-when-save-unicode-string-in-django
    # This alters the text field in order to handle the correct format. Change the VARCHAR(255) to VARCHAR(max_length_value)
    body = models.TextField(_('Body'), max_length=1000000, default='')

class SharedEntry(Entry):
    type = 'shared'
    entry = models.ForeignKey(Entry, related_name="shared")

class Comment(TimeStampedModel):
    entry = models.ForeignKey(Entry, related_name='comments')
    user = models.ForeignKey(User, related_name='comments')
    text = models.TextField('description', null=True, blank=True)


class Flagged(TimeStampedModel):
    entry = models.ForeignKey('Entry')
    reporter = models.ForeignKey(User)

    def __unicode__(self):
        return u'%s %s' % (self.entry.user, self.entry.text)
    def delete(self, delete_entry=True):
        # fetch entry object
        if delete_entry:
            entry = self.entry
            entry = Entry.objects.get(id=entry.id)
            entry.delete()
        return super(Flagged, self).delete()


