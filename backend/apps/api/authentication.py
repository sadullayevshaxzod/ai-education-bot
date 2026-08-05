"""
Authentication classes for the API.
"""

from __future__ import annotations

from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from apps.users.models import User


class TelegramAuthentication(BaseAuthentication):
    """
    Authenticate requests coming from the Telegram bot.
    """

    BOT_TOKEN_HEADER = "HTTP_X_BOT_TOKEN"
    TELEGRAM_ID_HEADER = "HTTP_X_TELEGRAM_ID"

    def authenticate(self, request):
        """
        Authenticate request using bot token and Telegram ID.
        """

        bot_token = request.META.get(self.BOT_TOKEN_HEADER)

        if bot_token != settings.BOT_API_TOKEN:
            raise AuthenticationFailed(
                "Invalid bot token.",
            )

        telegram_id = request.META.get(
            self.TELEGRAM_ID_HEADER,
        )

        if telegram_id is None:
            raise AuthenticationFailed(
                "Telegram ID header is missing.",
            )

        try:
            telegram_id = int(telegram_id)
        except (TypeError, ValueError):
            raise AuthenticationFailed(
                "Invalid Telegram ID.",
            )

        try:
            user = User.objects.get(
                telegram_id=telegram_id,
                is_active=True,
            )
        except User.DoesNotExist:
            raise AuthenticationFailed(
                "User not found.",
            )

        return (
            user,
            None,
        )