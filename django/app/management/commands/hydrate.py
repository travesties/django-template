from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Populates database with starting data"

    def handle(self, *args, **options):
        raise CommandError("hydrate not yet implemented!")