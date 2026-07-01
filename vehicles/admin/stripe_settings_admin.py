# ==========================================
# MyCarMarket
# Version: v1.4.8
# File: vehicles/admin/stripe_settings_admin.py
# Description: Stripe Settings Admin Control
# ==========================================

from django.contrib import admin

from vehicles.models import StripeSettings


@admin.register(StripeSettings)
class StripeSettingsAdmin(admin.ModelAdmin):

    fieldsets = (
        (
            'Stripe Status',
            {
                'fields': (
                    'is_enabled',
                    'test_mode',
                )
            }
        ),
        (
            'Stripe API Keys',
            {
                'fields': (
                    'publishable_key',
                    'secret_key',
                    'webhook_secret',
                )
            }
        ),
    )

    readonly_fields = (
        'updated_at',
    )

    def has_add_permission(self, request):
        return not StripeSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False