from __future__ import unicode_literals

from django.contrib import admin

from taggit.models import Tag, TaggedItem


class TaggedItemInline(admin.StackedInline):
    model = TaggedItem

class TagAdmin(admin.ModelAdmin):
    inlines = [
        TaggedItemInline
    ]
    list_display = ["name", "slug"]
    ordering = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}

    def save_model(self, request, obj, form, change):
        # in order to prevent same slugs and complications
        # rule will be all tags must be lowercase
        obj.name = obj.name.lower()
        super(TagAdmin, self).save_model(request, obj, form, change)



admin.site.register(Tag, TagAdmin)
