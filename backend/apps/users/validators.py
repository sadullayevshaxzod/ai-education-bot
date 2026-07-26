"""
Validators for the users application.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError


def validate_telegram_id(value: int) -> None:
    """
    Validate Telegram user ID.
    """
    if value <= 0:
        raise ValidationError(
            "Telegram ID must be greater than zero."
        )


def validate_xp(value: int) -> None:
    """
    Validate user experience points.
    """
    if value < 0:
        raise ValidationError(
            "XP cannot be negative."
        )