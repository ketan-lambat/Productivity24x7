from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from colorfield.fields import ColorField


# Create your models here.
class User(AbstractUser):
    # REQUIRED_FIELDS = ['username', 'email']

    def __str__(self):
        return self.username


class Tag(models.Model):
    priority = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(100)])
    name = models.CharField(max_length=25, blank=False)
    color = ColorField(default='#A8A8A8')

    def __str__(self):
        return self.name


class Reminder(models.Model):
    key = models.CharField(primary_key=True, max_length=25)
    message = models.CharField(max_length=100, blank=False)
    time = models.DateTimeField(auto_now=False, auto_now_add=False, blank=False)
    color = ColorField(default='#A8A8A8')
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message


class Task(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    managed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ForeignKey(Tag, blank=True, null=True, on_delete=models.SET_NULL)
    duration = models.PositiveIntegerField(blank=True, validators=[MinValueValidator(1), MaxValueValidator(10000)])
    deadline = models.DateTimeField(auto_now=False, blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
