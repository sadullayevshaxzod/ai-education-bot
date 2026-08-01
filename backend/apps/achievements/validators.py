"""
Custom validators for the achievements application.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError


def validate_required_level(value: int) -> None:
    """
    Validate required level.
    """
    if value < 1:
        raise ValidationError(
            "Required level must be greater than or equal to 1."
        )


def validate_xp_reward(value: int) -> None:
    """
    Validate XP reward.
    """
    if value < 0:
        raise ValidationError(
            "XP reward cannot be negative."
        )


def validate_achievement_name(value: str) -> None:
    """
    Validate achievement name.
    """
    value = value.strip()

    if len(value) < 3:
        raise ValidationError(
            "Achievement name must contain at least 3 characters."
        )

    if len(value) > 100:
        raise ValidationError(
            "Achievement name cannot exceed 100 characters."
        )