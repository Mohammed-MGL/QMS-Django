from django.apps import AppConfig
from django.conf import settings


class QmsAppConfig(AppConfig):
    name = 'QMS_app'

    def ready(self):
        import os
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="qmss-f3278-firebase-adminsdk-r8nrn-c52e600409.json"
    #     from . import scheduler
    #     if settings.SCHEDULER_AUTOSTART:
    #     	scheduler.start()