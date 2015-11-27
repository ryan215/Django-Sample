from django.contrib import admin
from datetime import datetime
from django.contrib import admin
from django.http import HttpResponse

from workouts.models import Video, VideoComment


class VideoAdmin(admin.ModelAdmin):
    """Admin for invitation code"""

    list_display = ('title', 'views', 'pub_date')

#admin.site.register(Invitation, InvitationAdmin)
admin.site.register(Video, VideoAdmin)


class VideoCommentAdmin(admin.ModelAdmin):
    """Admin for invitation code"""

    list_display = ('user','video','comment',)


admin.site.register(VideoComment, VideoCommentAdmin)
