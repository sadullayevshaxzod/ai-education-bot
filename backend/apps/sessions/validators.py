"""
Validators for the sessions application.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError


def validate_score(value: int) -> None:
    """
    Ensure that the score is not negative.
    """
    if value < 0:
        raise ValidationError(
            "Score cannot be negative."
        )


def validate_correct_answers(value: int) -> None:
    """
    Ensure that the number of correct answers is not negative.
    """
    if value < 0:
        raise ValidationError(
            "Correct answers cannot be negative."
        )


def validate_wrong_answers(value: int) -> None:
    """
    Ensure that the number of wrong answers is not negative.
    """
    if value < 0:
        raise ValidationError(
            "Wrong answers cannot be negative."
        )


def validate_xp_earned(value: int) -> None:
    """
    Ensure that earned XP is not negative.
    """
    if value < 0:
        raise ValidationError(
            "Earned XP cannot be negative."
        )