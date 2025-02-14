from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

INITIAL_USER_COUNT = getattr(settings, "INITIAL_USER_COUNT", 2)


class Command(BaseCommand):
    help = "Creates initial users"

    def handle(self, *args, **options):
        [
            User.objects.create_superuser(
                username=f"user{n + 1}",
                email=f"user{n + 1}@example.com",
                password="password",
            )
            for n in range(INITIAL_USER_COUNT)
        ]
