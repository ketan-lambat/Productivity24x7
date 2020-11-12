from django.contrib import admin
from .models import User, Tag, Task, Reminder
# Register your models here.

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Task)
admin.site.register(Reminder)
