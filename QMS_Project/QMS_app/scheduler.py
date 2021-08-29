import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from django_apscheduler.jobstores import register_events, register_job
from .scheduler_job import update_something ,delete_old_book , update_service_time

from django.conf import settings

# Create scheduler to run in a thread inside the application process
scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)

def start():
    # if settings.DEBUG:
      	# Hook into the apscheduler logger
        # logging.basicConfig()
        # logging.getLogger('apscheduler').setLevel(logging.DEBUG)


    # - replace_existing in combination with the unique ID prevents duplicate copies of the job

    scheduler.add_job(update_service_time, "interval", minutes= 1 ,id="job3",replace_existing=True)
    scheduler.add_job(update_something, "interval", minutes= 2 ,id="job1",replace_existing=True)
    scheduler.add_job(delete_old_book , 'cron' , hour=0 ,id="job2",replace_existing=True)

    # Add the scheduled jobs to the Django admin interface
    register_events(scheduler)

    scheduler.start()