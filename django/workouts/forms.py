#Django Libs
from django.contrib import auth
from django import forms
#Python Libs
from time import time, gmtime, strftime
#Models
from models import VideoComment, Video



class VideoCommentForm(forms.ModelForm):
    pub_date = forms.DateTimeField(initial = strftime("%m/%d/%y %H:%M", gmtime()))

    class Meta:
        model = VideoComment
        fields = ('video_id', 'user', 'comment', 'pub_date')


class VideoForm(forms.ModelForm):

    class Meta:
        model = Video
        fields = ('user', 'title', 'description', 'difficulty')

    def __init__(self, *args, **kargs):
        super(VideoForm, self).__init__(*args, **kargs)
