"""
Module for the Django app.

https://docs.djangoproject.com/en/5.1/ref/applications/
"""

from .celery import app as celery_app

__all__ = ("celery_app",)