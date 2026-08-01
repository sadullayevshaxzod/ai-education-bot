"""
Database models for the achievements application.
"""

from __future__ import annotations

from django.db import models

from apps.common.models import BaseModel
from apps.users.models import User

from .validators import (
    validate_achievement_name,
    validate_required_level,
    validate_xp_reward,
)


class Achievement(BaseModel):
    """
    Achievement that can be earned by users.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[validate_achievement_name],
        verbose_name="Name",
    )

    description = models.TextField(
        blank=True,
        default="",
        verbose_name="Description",
    )

    required_level = models.PositiveIntegerField(
        default=1,
        validators=[validate_required_level],
        verbose_name="Required level",
    )

    xp_reward = models.PositiveIntegerField(
        default=0,
        validators=[validate_xp_reward],
        verbose_name="XP reward",
    )

    icon = models.CharField(
        max_length=20,
        blank=True,
        default="🏆",
        verbose_name="Icon",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Is active",
    )

    class Meta:
        db_table = "achievements"
        verbose_name = "Achievement"
        verbose_name_plural = "Achievements"
        ordering = ["required_level", "name"]

    def __str__(self) -> str:
        return self.name


class UserAchievement(BaseModel):
    """
    Achievement earned by a user.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="achievements",
        verbose_name="User",
    )

    achievement = models.ForeignKey(
        Achievement,
        on_delete=models.CASCADE,
        related_name="users",
        verbose_name="Achievement",
    )

    earned_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Earned at",
    )

    class Meta:
        db_table = "user_achievements"
        verbose_name = "User Achievement"
        verbose_name_plural = "User Achievements"
        ordering = ["-earned_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["user", "achievement"],
                name="unique_user_achievement",
            )
        ]

    def __str__(self) -> str:
        return f"{self.user} - {self.achievement}"