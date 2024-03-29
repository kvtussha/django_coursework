import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email="admin@sky.pro",
            first_name="admin",
            last_name="adminov",
            is_staff=True,
            is_superuser=True,
            verification_code='123456',
        )
        user.set_password(os.getenv('POSTGRES_PASSWORD'))
        user.is_active = True
        user.save()
