# ==========================================
# MyCarMarket
# Version: v1.1.6
# File: vehicles/management/commands/daily_tasks.py
# Automatic Daily Background Tasks
# ==========================================

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils import timezone

from vehicles.models import Car


class Command(BaseCommand):

    help = 'Run all daily background tasks'

    def handle(self, *args, **kwargs):

        today = timezone.now()

        self.stdout.write(
            self.style.SUCCESS(
                f'Starting daily tasks ({today})'
            )
        )

        # ==========================================
        # 1. Check dealer expiry
        # ==========================================

        self.stdout.write(
            self.style.WARNING(
                'Checking dealer packages...'
            )
        )

        call_command('check_dealer_expiry')

        # ==========================================
        # 2. Remove expired featured cars
        # ==========================================

        expired_count = Car.objects.filter(
            is_featured=True,
            featured_until__isnull=False,
            featured_until__lt=today
        ).update(
            is_featured=False,
            featured_until=None
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Expired featured cars: {expired_count}'
            )
        )

        # ==========================================
        # Completed
        # ==========================================

        self.stdout.write(
            self.style.SUCCESS(
                'Daily tasks completed.'
            )
        )