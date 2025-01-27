import random

from app.db.routers import CeleryBeatRouter, ReplicationRouter
from app.tests.fixtures import *
from django_celery_beat.models import PeriodicTask

from django.contrib.auth.models import User


def test_celerybeat_router():
    """
    Database router tests to ensure that database operations
    on django_celery_beat models are routed to the celerybeat
    database.
    """
    router = CeleryBeatRouter()

    assert router.db_for_read(PeriodicTask) == "celerybeat"
    assert router.db_for_read(User) is None

    assert router.db_for_write(PeriodicTask) == "celerybeat"
    assert router.db_for_write(User) is None

    # Relations are not allowed with models outside django_celery_beat
    assert router.allow_relation(PeriodicTask, PeriodicTask) is True
    assert router.allow_relation(PeriodicTask, User) is False
    assert router.allow_relation(User, User) is None

    assert router.allow_migrate("celerybeat", "django_celery_beat") is True
    assert router.allow_migrate("default", "django_celery_beat") is False
    assert router.allow_migrate("celerybeat", "auth") is False
    assert router.allow_migrate("default", "auth") is None


def test_replication_router(monkeypatch):
    """
    Database router tests to ensure that read and write requests
    are correctly routed to the primary and replicated databases.
    """
    router = ReplicationRouter()

    assert router.db_for_read(User) is not None
    assert router.db_for_read(PeriodicTask) is None

    # Force random.choice to return the 0th index db alias
    monkeypatch.setattr(random, "choice", lambda arr: arr[0])
    assert router.db_for_read(User) == "default"
    assert router.db_for_read(PeriodicTask) is None

    # Force random.choice to return the 1st index db alias
    monkeypatch.setattr(random, "choice", lambda arr: arr[1])
    assert router.db_for_read(User) == "replica"
    assert router.db_for_read(PeriodicTask) is None

    # Writes should always go to "default"
    assert router.db_for_write(User) == "default"
    assert router.db_for_write(PeriodicTask) is None

    # Relations are not allowed with models outside supported apps.
    assert router.allow_relation(User, User) is True
    assert router.allow_relation(User, PeriodicTask) is False
    assert router.allow_relation(PeriodicTask, PeriodicTask) is None

    # Supported app models should only be migrated in "default".
    # Migrations should not be applied to unsupported models.
    assert router.allow_migrate("default", "auth") is True
    assert router.allow_migrate("default", "django_celery_beat") is False
    assert router.allow_migrate("replica", "auth") is False
    assert router.allow_migrate("replica", "django_celery_beat") is False
    assert router.allow_migrate("replica-1", "auth") is False
    assert router.allow_migrate("celerybeat", "auth") is False
    assert router.allow_migrate("celerybeat", "django_celery_beat") is None
