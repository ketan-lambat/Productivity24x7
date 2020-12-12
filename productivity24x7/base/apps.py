from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = 'base'

    def ready(self):
        from django.db.models.signals import post_save
        from .webhook import webhook
        from .models import Event
        post_save.connect(webhook, sender=Event, dispatch_uid="webhook_event_add")
