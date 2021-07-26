import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from django_apscheduler.jobstores import register_events, register_job
from .kokotest import update_something

from django.conf import settings

# Create scheduler to run in a thread inside the application process
scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)

def start():
    # if settings.DEBUG:
      	# Hook into the apscheduler logger
        # logging.basicConfig()
        # logging.getLogger('apscheduler').setLevel(logging.DEBUG)


    # - replace_existing in combination with the unique ID prevents duplicate copies of the job

    scheduler.add_job(update_something, "interval", minutes=1 ,id="job1",replace_existing=True)

    # Add the scheduled jobs to the Django admin interface
    register_events(scheduler)

    scheduler.start()