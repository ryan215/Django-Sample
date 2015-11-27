from django.contrib import admin

from schedule.models import Event, Rule


class EventAdmin(admin.ModelAdmin):
    list_display = ('creator', 'title','start', 'end')


admin.site.register(Event, EventAdmin)
