import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

app = Celery("app")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Create periodic task schedule.
# https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html#entries
app.conf.beat_schedule = {
    "greeting-task-execution": {
        "task": "app.tasks.greeting_task",
        "schedule": crontab(minute="*/2"),
        "args": (["Travis"]),
    },
    "debug-task-execution": {
        "task": "app.celery.debug_task",
        "schedule": 10.0,
        "args": (),
    },
}

# Set timezone for scheduled tasks if different from UTC
# https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html#time-zones
app.conf.timezone = "America/New_York"


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
