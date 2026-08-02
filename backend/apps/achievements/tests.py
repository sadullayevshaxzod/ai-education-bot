"""
Tests for the achievements application.
"""

from __future__ import annotations

from django.test import TestCase

from apps.common.choices import Language
from apps.users.choices import UserRole
from apps.users.models import User

from .models import (
    Achievement,
    UserAchievement,
)
from .services import AchievementService


class AchievementServiceTests(TestCase):
    """
    Tests for AchievementService.
    """

    def setUp(self) -> None:
        self.user = User.objects.create(
            telegram_id=123456789,
            username="test_user",
            first_name="Test",
            last_name="User",
            language=Language.UZ,
            role=UserRole.STUDENT,
            xp=0,
            level=3,
        )

        self.achievement = Achievement.objects.create(
            name="Python Beginner",
            description="Reach level 3.",
            required_level=3,
            xp_reward=100,
        )

    def test_unlock_achievement(self) -> None:
        """
        Should unlock an achievement.
        """
        user_achievement = AchievementService.unlock_achievement(
            user=self.user,
            achievement=self.achievement,
        )

        self.assertIsNotNone(user_achievement)

        self.assertTrue(
            UserAchievement.objects.filter(
                user=self.user,
                achievement=self.achievement,
            ).exists()
        )

    def test_unlock_achievement_only_once(self) -> None:
        """
        User should not receive the same achievement twice.
        """
        AchievementService.unlock_achievement(
            self.user,
            self.achievement,
        )

        AchievementService.unlock_achievement(
            self.user,
            self.achievement,
        )

        self.assertEqual(
            UserAchievement.objects.count(),
            1,
        )

    def test_unlock_achievement_adds_xp(self) -> None:
        """
        Unlocking an achievement should add XP.
        """
        AchievementService.unlock_achievement(
            self.user,
            self.achievement,
        )

        self.user.refresh_from_db()

        self.assertEqual(
            self.user.xp,
            100,
        )

    def test_has_achievement(self) -> None:
        """
        Should return True if the user already has the achievement.
        """
        AchievementService.unlock_achievement(
            self.user,
            self.achievement,
        )

        self.assertTrue(
            AchievementService.has_achievement(
                self.user,
                self.achievement,
            )
        )

    def test_check_level_achievements(self) -> None:
        """
        Should unlock achievements available for the user's level.
        """
        unlocked = AchievementService.check_level_achievements(
            self.user,
        )

        self.assertEqual(
            len(unlocked),
            1,
        )

        self.assertEqual(
            unlocked[0].achievement,
            self.achievement,
        )