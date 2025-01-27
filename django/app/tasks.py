from celery import shared_task
from celery.signals import beat_init
from celery.utils.log import get_task_logger
from django_celery_beat.models import PeriodicTask

logger = get_task_logger(__name__)


@beat_init.connect
def on_beat_init(sender=None, **kwargs):
    """
    Perform any work that should be done when celery beat is fully initialized.
    """
    scheduler = sender.get_scheduler() if sender else None
    beat_logger = scheduler.logger if scheduler else logger

    try:
        periodic_task = PeriodicTask.objects.get(name="task-name")
    except PeriodicTask.DoesNotExist:
        pass


@shared_task
def greeting_task(name):
    logger.debug(f"Hello, {name}!")
