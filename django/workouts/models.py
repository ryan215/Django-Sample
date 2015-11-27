#Django Libs
from django.db import models
#Python Libs
from time import time, gmtime, strftime
from user_app.models import Professional
from django.contrib.auth import get_user_model
User = get_user_model()
# from tagging.fields import TagField
from taggit.managers import TaggableManager
import datetime
from django.db.models import permalink
from django.contrib.comments.moderation import CommentModerator, moderator
from django.utils.timezone import now
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


# fs = FileSystemStorage(location='/home/miguel/Desktop/')


#Video Model
class Video(models.Model):
    user = models.ForeignKey(Professional, related_name='videos', blank=True,null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True,null=True)
    title = models.CharField(max_length = 200, blank=True,null=True)
    description = models.TextField('description', null=True, blank=True)
    pub_date = models.DateTimeField('date published', default=now, null=True, blank=True)
    url_video = models.CharField(max_length = 200, blank=True,null=True)
    img = models.ImageField(upload_to="workout", blank=True, default='default-profile.svg')
    video_tags = TaggableManager(blank=True, verbose_name='video')
    likes = models.IntegerField(blank=True, null=True, default=0)
    likes_user = models.ManyToManyField(User, related_name='video_like', blank=True,null=True)
    views = models.IntegerField(blank=True, null=True, default=0)
    # file = models.FileField(upload_to='videos', storage=fs, blank=True, null=True)

    DIFFICULTY_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    )
    difficulty = models.CharField(max_length=30, blank=True, choices=DIFFICULTY_CHOICES, default='beginner')


    #Metadata
    def __unicode__(self):
        return self.title


# @receiver(pre_delete, sender=Video)
# def video_delete(sender, instance, **kwargs):
#     instance.file.delete(False)


#Video Model
class VideoComment(models.Model):
    user = models.ForeignKey(User, blank=True,null=True)
    video =  models.ForeignKey(Video, related_name="comments")
    comment = models.TextField('description', null=True, blank=True)
    pub_date = models.DateTimeField('date published', default=now, null=True, blank=True)


    #Metadata











