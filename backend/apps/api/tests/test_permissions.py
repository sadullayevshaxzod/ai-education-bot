"""
Tests for API permissions.
"""

from __future__ import annotations

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.common.choices import Language
from apps.users.choices import UserRole
from apps.users.models import User


class PermissionTests(APITestCase):
    """
    Test API permissions.
    """

    def setUp(self) -> None:
        self.user = User.objects.create(
            telegram_id=123456789,
            username="testuser",
            first_name="Test",
            last_name="User",
            language=Language.UZ,
            role=UserRole.STUDENT,
            is_active=True,
        )

        self.inactive_user = User.objects.create(
            telegram_id=987654321,
            username="inactive",
            first_name="Inactive",
            last_name="User",
            language=Language.UZ,
            role=UserRole.STUDENT,
            is_active=False,
        )

        self.profile_url = reverse("api:user-profile")

    def test_anonymous_user_is_not_allowed(self) -> None:
        """
        Anonymous users should receive HTTP 401.
        """

        response = self.client.get(self.profile_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_authenticated_active_user_is_allowed(self) -> None:
        """
        Active authenticated users should access the endpoint.
        """

        self.client.force_authenticate(
            user=self.user,
        )

        response = self.client.get(self.profile_url)

        self.assertNotEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.assertNotEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_inactive_user_is_forbidden(self) -> None:
        """
        Inactive users should receive HTTP 403.
        """

        self.client.force_authenticate(
            user=self.inactive_user,
        )

        response = self.client.get(self.profile_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )