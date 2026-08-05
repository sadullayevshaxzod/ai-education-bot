"""
Serializers for achievement-related API endpoints.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.achievements.models import (
    Achievement,
    UserAchievement,
)


class AchievementSerializer(serializers.ModelSerializer):
    """
    Serializer for achievements.
    """

    class Meta:
        model = Achievement
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "required_level",
            "xp_reward",
        )
        read_only_fields = (
            "id",
        )


class UserAchievementSerializer(serializers.ModelSerializer):
    """
    Serializer for user achievements.
    """

    achievement = AchievementSerializer(
        read_only=True,
    )

    class Meta:
        model = UserAchievement
        fields = (
            "id",
            "achievement",
            "earned_at",
        )
        read_only_fields = (
            "id",
            "earned_at",
        )