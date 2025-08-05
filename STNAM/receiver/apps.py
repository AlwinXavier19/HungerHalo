from django.apps import AppConfig


class ReceiverConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'receiver'
# receiver/apps.py
from django.apps import AppConfig

class ReceiverConfig(AppConfig):
    name = 'receiver'

    def ready(self):
        import receiver.signals
