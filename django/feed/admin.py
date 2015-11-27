from django.contrib import admin
from django.core.urlresolvers import reverse
from feed.models import Entry, PhotoEntry, VideoEntry, BlogEntry, TextEntry, SharedEntry
from feed. models import Comment, Flagged

class FeedAdmin(admin.ModelAdmin):
    list_display = ('creator', 'title','start', 'end')

class EntryAdmin(admin.ModelAdmin):
    pass

class TextEntryAdmin(admin.ModelAdmin):
    pass
class PhotoEntryAdmin(admin.ModelAdmin):
    pass
class VideoEntryAdmin(admin.ModelAdmin):
    pass
class BlogEntryAdmin(admin.ModelAdmin):
    pass
class SharedEntryAdmin(admin.ModelAdmin):
    pass
class CommentAdmin(admin.ModelAdmin):
    pass
class EntryInline(admin.TabularInline):
    model = Entry


class FlaggedAdmin(admin.ModelAdmin):
    list_display = ('entry_user', "entry_id", "reporter_user",)
    readonly_fields = ('entry_user', 'entry_text', 'entry_object_link',)
    fields = ("entry_user", "entry_text", 'entry', 'reporter', 'entry_object_link')
    actions = ['approved']
    def entry_id(self, obj):
        return obj.entry.id
    entry_id.short_description = "Entry ID"
    def entry_user(self, obj):
        return obj.entry.user.email
    entry_user.short_description = "Entry by"
    def entry_text(self, obj):
        return obj.entry.text
    entry_text.short_description = "Body"
    def reporter_user(self, obj):
        return obj.reporter.email
    reporter_user.short_description = "Reported by"

    def entry_object_link(self, object):
        # gets the subclass of entry to go to proper view
        sub = Entry.objects.get_subclass(id=object.entry.id)
        url = reverse('admin:%s_%sentry_change' %(object._meta.app_label, sub.type),  args=[object.entry.id] )
        print url
        return '<a href="%s">Edit %s</a>' %(url,  object.__unicode__())
    entry_object_link.short_description = "Link to Entry obj"


    def approved(self, request, queryset):
        for obj in queryset:
            obj.delete(False)

    entry_object_link.allow_tags = True

admin.site.register(Entry, EntryAdmin)
admin.site.register(TextEntry, TextEntryAdmin)
admin.site.register(PhotoEntry, PhotoEntryAdmin)
admin.site.register(VideoEntry, VideoEntryAdmin)
admin.site.register(BlogEntry, BlogEntryAdmin)
admin.site.register(SharedEntry, SharedEntryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Flagged, FlaggedAdmin)
