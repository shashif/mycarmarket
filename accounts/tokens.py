# ==========================================
# MyCarMarket
# Version: v1.6.5
# File: accounts/tokens.py
# Description: Email Verification Token
# ==========================================

from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_active)


email_verification_token = EmailVerificationTokenGenerator()