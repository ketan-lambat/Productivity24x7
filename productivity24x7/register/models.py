from django.core.validators import validate_email
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

from .manager import UserManager


class User(AbstractBaseUser):
    first_name = models.CharField(blank=False, max_length=30, verbose_name="First Name")
    last_name = models.CharField(blank=True, max_length=30, verbose_name="Last Name", default="")
    email = models.EmailField(blank=False, unique=True, verbose_name="E-mail")
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def has_perm(self, perm, obj=None):
        if self.is_superuser or self.is_staff:
            return True
        else:
            return False

    def has_module_perms(self, app_label):
        if self.is_superuser or self.is_staff:
            return True
        else:
            return False

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name']

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def repr(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def full_clean(self, exclude=None, validate_unique=True):
        validate_email(self.email)
        super().full_clean(exclude=exclude, validate_unique=validate_unique)
