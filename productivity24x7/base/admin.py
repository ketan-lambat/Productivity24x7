from django.contrib import admin
from .models import User, Tag, Task, Event

# Register your models here.

admin.site.register(Tag)
admin.site.register(Task)
admin.site.register(Event)
