"""
Business logic for the achievements application.
"""

from __future__ import annotations

from django.db import transaction

from apps.users.services import UserService

from .models import (
    Achievement,
    UserAchievement,
)


class AchievementService:
    """
    Service layer for achievements.
    """

    @staticmethod
    def has_achievement(user, achievement) -> bool:
        """
        Check whether a user already has an achievement.
        """
        return UserAchievement.objects.filter(
            user=user,
            achievement=achievement,
        ).exists()

    @staticmethod
    @transaction.atomic
    def unlock_achievement(user, achievement) -> UserAchievement | None:
        """
        Unlock an achievement for a user.
        """

        if AchievementService.has_achievement(
            user,
            achievement,
        ):
            return None

        user_achievement = UserAchievement.objects.create(
            user=user,
            achievement=achievement,
        )

        UserService.add_xp(
            user=user,
            xp=achievement.xp_reward,
        )

        return user_achievement

    @staticmethod
    def check_level_achievements(user) -> list[UserAchievement]:
        """
        Unlock all achievements available for the user's level.
        """

        unlocked = []

        achievements = Achievement.objects.filter(
            is_active=True,
            required_level__lte=user.level,
        )

        for achievement in achievements:
            user_achievement = AchievementService.unlock_achievement(
                user=user,
                achievement=achievement,
            )

            if user_achievement:
                unlocked.append(user_achievement)

        return unlocked