from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ObjectDoesNotExist


class UserManager(BaseUserManager):
    def _create_user(self, first_name, email, last_name="", password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set.')
        email = self.normalize_email(email)
        user = self.model(first_name=first_name, last_name=last_name, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, first_name, email, last_name="", password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(first_name, email, last_name, password, **extra_fields)

    def create_superuser(self, first_name, email, last_name="", password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(first_name, email, last_name, password, **extra_fields)

    def get_or_none(self, *args, **kwargs):
        try:
            u = self.get(*args, **kwargs)
            return u
        except ObjectDoesNotExist:
            return None
