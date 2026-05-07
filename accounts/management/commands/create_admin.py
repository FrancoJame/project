from django.core.management.base import BaseCommand
from accounts.models import CustomUser
import os

class Command(BaseCommand):
    help = 'Creates a default admin user if it does not exist'

    def handle(self, *args, **options):
        username = 'admin'
        password = 'admin1234'
        email = 'admin@example.com'

        if not CustomUser.objects.filter(username=username).exists():
            self.stdout.write(f'Creating superuser {username}...')
            CustomUser.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                role='MANAGER'
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser {username}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser {username} already exists'))
