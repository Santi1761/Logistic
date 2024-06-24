from django.contrib import admin


from .models import Event
from .models import Task


class EventAdmin(admin.ModelAdmin):
    readonly_fields = ("registerDate", )


admin.site.register(Event, EventAdmin)
admin.site.register(Task)
