from colorfield.fields import ColorField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
import re
from django.db import transaction

from register.models import User


class Tag(models.Model):
    priority = models.PositiveIntegerField()
    name = models.CharField(max_length=25, blank=False)
    color = ColorField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return self.name

    def clean(self):
        val = self.name
        if isinstance(val, str) and re.match('^[A-Za-z][A-Za-z_]*$', val):
            self.name = str(val).lower()
        else:
            raise ValidationError({'name': 'Not a valid tag name.'})

    class Meta:
        unique_together = (('owner', 'name'),)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        super(Tag, self).save(force_insert=force_insert, force_update=force_update, using=using,
                              update_fields=update_fields)


class Task(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    duration = models.PositiveIntegerField(null=True, default=None, help_text="in minutes")
    deadline = models.DateTimeField(auto_now=False, null=True, default=None)
    is_completed = models.BooleanField(default=None, null=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, editable=False)
    g_event_id = models.CharField(max_length=100, blank=True, null=True, default=None)

    def __str__(self):
        return self.title

    def clean(self):
        if self.start > self.end:
            raise ValidationError({'start': "Start Time must be before End Time."})

    @transaction.atomic
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        super(Event, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                update_fields=update_fields)
        ts = getattr(self, "__tags", None)
        if ts is not None:
            self.save_tags(ts)

    def tags_get(self):
        x = []
        for t in self._tags.all():
            x.append(str(t.tag.name))
        return x

    def tags_set(self, val):
        setattr(self, "__tags", val)

    tags = property(fget=tags_get, fset=tags_set)

    @transaction.atomic
    def save_tags(self, value):
        if isinstance(value, (list, tuple)):
            for i in value:
                if not isinstance(i, str):
                    raise ValidationError({'tags': "Tags must be valid string."})
            EventTags.objects.filter(event__pk=self.pk).delete()
            for i in value:
                if Tag.objects.filter(owner__pk=self.owner.pk, name=str(i)).exists():
                    t = Tag.objects.get(owner__pk=self.owner.pk, name=str(i))
                    EventTags(event=self, tag=t).save()
                else:
                    raise ValidationError({'tags': "Tag Does Not Exist."})
        else:
            raise ValidationError({'tags': "Tags must be a list of array."})


class EventTags(models.Model):
    tag = models.ForeignKey(to=Tag, related_name="events", on_delete=models.CASCADE)
    event = models.ForeignKey(to=Event, related_name="_tags", on_delete=models.CASCADE)
