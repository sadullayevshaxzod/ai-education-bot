"""
Unit tests for TelegramAuthentication.
"""

from __future__ import annotations

from django.conf import settings
from django.test import TestCase, override_settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APIRequestFactory

from apps.api.authentication import TelegramAuthentication
from apps.common.choices import Language
from apps.users.choices import UserRole
from apps.users.models import User


@override_settings(
    BOT_API_TOKEN="test-secret-token",
)
class TelegramAuthenticationTests(TestCase):
    """
    Unit tests for TelegramAuthentication.
    """

    def setUp(self):
        self.factory = APIRequestFactory()

        self.authentication = TelegramAuthentication()

        self.user = User.objects.create(
            telegram_id=123456789,
            username="testuser",
            first_name="Test",
            last_name="User",
            language=Language.UZ,
            role=UserRole.STUDENT,
            is_active=True,
        )

    def test_successful_authentication(self):
        """
        Valid token and telegram id should authenticate user.
        """

        request = self.factory.get(
            "/",
            HTTP_X_BOT_TOKEN=settings.BOT_API_TOKEN,
            HTTP_X_TELEGRAM_ID=str(self.user.telegram_id),
        )

        user, auth = self.authentication.authenticate(
            request,
        )

        self.assertEqual(
            user,
            self.user,
        )

        self.assertIsNone(
            auth,
        )

    def test_invalid_bot_token(self):
        """
        Invalid bot token should raise AuthenticationFailed.
        """

        request = self.factory.get(
            "/",
            HTTP_X_BOT_TOKEN="wrong-token",
            HTTP_X_TELEGRAM_ID=str(self.user.telegram_id),
        )

        with self.assertRaises(AuthenticationFailed):
            self.authentication.authenticate(
                request,
            )

    def test_missing_bot_token(self):
        """
        Missing bot token should raise AuthenticationFailed.
        """

        request = self.factory.get(
            "/",
            HTTP_X_TELEGRAM_ID=str(self.user.telegram_id),
        )

        with self.assertRaises(AuthenticationFailed):
            self.authentication.authenticate(
                request,
            )

    def test_missing_telegram_id(self):
        """
        Missing telegram id should raise AuthenticationFailed.
        """

        request = self.factory.get(
            "/",
            HTTP_X_BOT_TOKEN=settings.BOT_API_TOKEN,
        )

        with self.assertRaises(AuthenticationFailed):
            self.authentication.authenticate(
                request,
            )

    def test_invalid_telegram_id(self):
        """
        Invalid telegram id should raise AuthenticationFailed.
        """

        request = self.factory.get(
            "/",
            HTTP_X_BOT_TOKEN=settings.BOT_API_TOKEN,
            HTTP_X_TELEGRAM_ID="abc",
        )

        with self.assertRaises(AuthenticationFailed):
            self.authentication.authenticate(
                request,
            )

    def test_user_not_found(self):
        """
        Unknown telegram user should raise AuthenticationFailed.
        """

        request = self.factory.get(
            "/",
            HTTP_X_BOT_TOKEN=settings.BOT_API_TOKEN,
            HTTP_X_TELEGRAM_ID="999999999",
        )

        with self.assertRaises(AuthenticationFailed):
            self.authentication.authenticate(
                request,
            )

    def test_inactive_user(self):
        """
        Inactive user should raise AuthenticationFailed.
        """

        self.user.is_active = False
        self.user.save()

        request = self.factory.get(
            "/",
            HTTP_X_BOT_TOKEN=settings.BOT_API_TOKEN,
            HTTP_X_TELEGRAM_ID=str(self.user.telegram_id),
        )

        with self.assertRaises(AuthenticationFailed):
            self.authentication.authenticate(
                request,
            )