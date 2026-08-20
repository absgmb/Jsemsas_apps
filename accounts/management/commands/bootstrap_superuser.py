import os

from django.core.management.base import BaseCommand, CommandError
from accounts.models import User


class Command(BaseCommand):
    help = "Create or update the initial J-SEMSAS superuser from environment variables."

    def handle(self, *args, **options):
        username = os.getenv("BOOTSTRAP_SUPERUSER_USERNAME", "").strip()
        password = os.getenv("BOOTSTRAP_SUPERUSER_PASSWORD", "")
        email = os.getenv("BOOTSTRAP_SUPERUSER_EMAIL", "admin@jsemsas.local").strip()

        if not username or not password:
            self.stdout.write(self.style.WARNING(
                "Bootstrap superuser skipped: BOOTSTRAP_SUPERUSER_USERNAME and/or BOOTSTRAP_SUPERUSER_PASSWORD is not set."
            ))
            return

        user, created = User.objects.get_or_create(username=username)
        user.email = email
        user.role = User.Roles.SUPER_ADMIN
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{action} bootstrap superuser '{username}'."))
