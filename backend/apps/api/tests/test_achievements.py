"""
Tests for achievement API endpoints.
"""

from __future__ import annotations

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.common.choices import Language
from apps.achievements.models import (
    Achievement,
    UserAchievement,
)
from apps.users.choices import UserRole
from apps.users.models import User


class AchievementAPITests(APITestCase):
    """
    Tests for achievement API endpoints.
    """

    def setUp(self) -> None:
        self.user = User.objects.create(
            telegram_id=123456789,
            username="testuser",
            first_name="Test",
            last_name="User",
            language=Language.UZ,
            role=UserRole.STUDENT,
            level=5,
            is_active=True,
        )

        self.client.force_authenticate(
            user=self.user,
        )

        self.achievement = Achievement.objects.create(
            name="First Lesson",
            description="Complete your first lesson.",
            icon="🏆",
            xp_reward=100,
            required_level=1,
        )

        self.list_url = reverse(
            "api:achievement-list",
        )

        self.detail_url = reverse(
            "api:achievement-detail",
            kwargs={
                "achievement_id": self.achievement.id,
            },
        )

        self.user_list_url = reverse(
            "api:user-achievements",
        )

        self.unlock_url = reverse(
            "api:unlock-achievement",
            kwargs={
                "achievement_id": self.achievement.id,
            },
        )

        self.check_url = reverse(
            "api:check-achievements",
        )

    def test_get_achievements(self) -> None:
        """
        Should return achievements.
        """

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"],
        )

        self.assertEqual(
            len(response.data["data"]),
            1,
        )

    def test_get_achievement_detail(self) -> None:
        """
        Should return achievement detail.
        """

        response = self.client.get(
            self.detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["data"]["name"],
            self.achievement.name,
        )

    def test_unlock_achievement(self) -> None:
        """
        Should unlock achievement.
        """

        response = self.client.post(
            self.unlock_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            UserAchievement.objects.count(),
            1,
        )

    def test_get_user_achievements(self) -> None:
        """
        Should return user achievements.
        """

        UserAchievement.objects.create(
            user=self.user,
            achievement=self.achievement,
        )

        response = self.client.get(
            self.user_list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data["data"]),
            1,
        )

    def test_check_level_achievements(self) -> None:
        """
        Should unlock achievements for the current level.
        """

        response = self.client.post(
            self.check_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            UserAchievement.objects.count(),
            1,
        )

    def test_requires_authentication(self) -> None:
        """
        Anonymous users should not access achievement endpoints.
        """

        self.client.force_authenticate(
            user=None,
        )

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )