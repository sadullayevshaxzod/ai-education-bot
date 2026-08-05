"""
Business logic for the achievements application.
"""

from __future__ import annotations

from django.db import transaction
from django.db.models import QuerySet

from apps.users.models import User
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
    def get_achievements() -> QuerySet[Achievement]:
        """
        Return all active achievements.
        """
        return Achievement.objects.filter(
            is_active=True,
        ).order_by(
            "required_level",
            "id",
        )

    @staticmethod
    def get_achievement(
        achievement_id: int,
    ) -> Achievement:
        """
        Return an achievement by ID.
        """
        return Achievement.objects.get(
            pk=achievement_id,
            is_active=True,
        )

    @staticmethod
    def get_user_achievements(
        user: User,
    ) -> QuerySet[UserAchievement]:
        """
        Return all achievements unlocked by a user.
        """
        return (
            UserAchievement.objects.filter(
                user=user,
            )
            .select_related("achievement")
            .order_by("-created_at")
        )

    @staticmethod
    def has_achievement(
        user: User,
        achievement: Achievement,
    ) -> bool:
        """
        Check whether a user already has an achievement.
        """
        return UserAchievement.objects.filter(
            user=user,
            achievement=achievement,
        ).exists()

    @staticmethod
    @transaction.atomic
    def unlock_achievement(
        user: User,
        achievement: Achievement,
    ) -> UserAchievement | None:
        """
        Unlock an achievement for a user.
        """

        if AchievementService.has_achievement(
            user=user,
            achievement=achievement,
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
    @transaction.atomic
    def check_level_achievements(
        user: User,
    ) -> list[UserAchievement]:
        """
        Unlock all achievements available for the user's level.
        """

        unlocked: list[UserAchievement] = []

        achievements = AchievementService.get_achievements().filter(
            required_level__lte=user.level,
        )

        for achievement in achievements:
            user_achievement = AchievementService.unlock_achievement(
                user=user,
                achievement=achievement,
            )

            if user_achievement is not None:
                unlocked.append(user_achievement)

        return unlocked