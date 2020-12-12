from django.contrib import admin
from .models import EventTags, Tag, Task, Event

# Register your models here.

admin.site.register(Tag)
admin.site.register(Task)
admin.site.register(Event)
admin.site.register(EventTags)
