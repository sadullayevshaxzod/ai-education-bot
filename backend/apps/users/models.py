"""
Database models for the users application.
"""

from __future__ import annotations

from django.db import models
from django.utils import timezone

from apps.common.models import BaseModel
from apps.common.choices import Language
from .choices import UserRole
from .validators import (
    validate_telegram_id,
    validate_xp,
)


class User(BaseModel):
    """
    Telegram user.
    """

    telegram_id = models.BigIntegerField(
        unique=True,
        validators=[validate_telegram_id],
        verbose_name="Telegram ID",
    )

    username = models.CharField(
        max_length=32,
        blank=True,
        default="",
        verbose_name="Username",
    )

    first_name = models.CharField(
        max_length=100,
        verbose_name="First name",
    )

    last_name = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Last name",
    )

    language = models.CharField(
        max_length=5,
        choices=Language.choices,
        default=Language.UZ,
        verbose_name="Language",
    )

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.STUDENT,
        verbose_name="Role",
    )

    xp = models.PositiveIntegerField(
        default=0,
        validators=[validate_xp],
        verbose_name="Experience",
    )

    level = models.PositiveIntegerField(
        default=1,
        verbose_name="Level",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Is active",
    )

    last_activity = models.DateTimeField(
        default=timezone.now,
        verbose_name="Last activity",
    )

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_anonymous(self) -> bool:
        return False

    def __str__(self) -> str:
        return (
            self.username
            if self.username
            else str(self.telegram_id)
        )