from django.apps import AppConfig
from django.conf import settings


class QmsAppConfig(AppConfig):
    name = 'QMS_app'

    # def ready(self):
    #     from . import scheduler
    #     if settings.SCHEDULER_AUTOSTART:
    #     	scheduler.start()