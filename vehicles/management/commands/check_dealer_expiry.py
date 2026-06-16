
# ==========================================
# MyCarMarket
# Version: v1.1.5
# File: vehicles/management/commands/check_dealer_expiry.py
# Automatic Dealer Package Expiry Checker
# ==========================================

from django.core.management.base import BaseCommand
from django.utils import timezone

from vehicles.models import DealerProfile, Car


class Command(BaseCommand):

    help = 'Automatically deactivate expired dealer packages'

    def handle(self, *args, **kwargs):

        now = timezone.now()

        expired_dealers = DealerProfile.objects.filter(
            package_active=True,
            package_expiry__isnull=False,
            package_expiry__lt=now
        )

        if not expired_dealers.exists():

            self.stdout.write(
                self.style.SUCCESS(
                    'No expired dealer packages found.'
                )
            )

            return

        count = 0

        for dealer in expired_dealers:

            # Reset dealer package

            dealer.package = 'free'

            dealer.package_active = False

            dealer.is_dealer = False

            dealer.is_featured_dealer = False

            dealer.max_listings = 3

            dealer.featured_ads_allowed = 0

            dealer.priority_support = False

            dealer.save()

            # Remove featured cars

            Car.objects.filter(
                seller=dealer.user,
                is_featured=True
            ).update(
                is_featured=False,
                featured_until=None
            )

            count += 1

            self.stdout.write(
                self.style.WARNING(
                    f'Expired: {dealer.user.username}'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'{count} dealer package(s) deactivated.'
            )
        )