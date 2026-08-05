"""
Tests for user API endpoints.
"""

from __future__ import annotations

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.common.choices import Language
from apps.users.choices import UserRole
from apps.users.models import User


class UserAPITests(APITestCase):
    """
    Tests for user API endpoints.
    """

    def setUp(self) -> None:
        self.user = User.objects.create(
            telegram_id=123456789,
            username="testuser",
            first_name="Test",
            last_name="User",
            language=Language.UZ,
            role=UserRole.STUDENT,
            xp=150,
            level=2,
            is_active=True,
        )

        self.client.force_authenticate(
            user=self.user,
        )

        self.profile_url = reverse(
            "api:user-profile",
        )

        self.update_url = reverse(
            "api:user-update",
        )

        self.leaderboard_url = reverse(
            "api:leaderboard",
        )

    def test_get_profile(self) -> None:
        """
        Should return the authenticated user profile.
        """

        response = self.client.get(
            self.profile_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["data"]["telegram_id"],
            self.user.telegram_id,
        )

        self.assertEqual(
            response.data["data"]["username"],
            self.user.username,
        )

    def test_update_profile(self) -> None:
        """
        Should update the authenticated user.
        """

        payload = {
            "username": "new_username",
            "first_name": "Updated",
            "last_name": "User",
            "language": Language.EN,
        }

        response = self.client.patch(
            self.update_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.user.refresh_from_db()

        self.assertEqual(
            self.user.username,
            payload["username"],
        )

        self.assertEqual(
            self.user.first_name,
            payload["first_name"],
        )

        self.assertEqual(
            self.user.language,
            payload["language"],
        )

    def test_get_leaderboard(self) -> None:
        """
        Should return leaderboard.
        """

        response = self.client.get(
            self.leaderboard_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertGreaterEqual(
            len(response.data["data"]),
            1,
        )

    def test_profile_requires_authentication(self) -> None:
        """
        Anonymous users should not access profile.
        """

        self.client.force_authenticate(
            user=None,
        )

        response = self.client.get(
            self.profile_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_update_requires_authentication(self) -> None:
        """
        Anonymous users should not update profile.
        """

        self.client.force_authenticate(
            user=None,
        )

        response = self.client.patch(
            self.update_url,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )