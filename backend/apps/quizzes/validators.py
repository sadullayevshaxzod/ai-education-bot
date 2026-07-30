"""
Validators for the quizzes application.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError


def validate_points(value: int) -> None:
    """
    Ensure that question points are positive.
    """
    if value <= 0:
        raise ValidationError(
            "Points must be greater than zero."
        )