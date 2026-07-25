"""
Reusable validators for the project.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError

from .constants import (
    MAX_IMAGE_SIZE,
    ALLOWED_IMAGE_EXTENSIONS,
    MIN_SCORE,
    MAX_SCORE,
)


def validate_positive(value: int | float) -> None:
    """
    Validate that the value is zero or greater.
    """
    if value < 0:
        raise ValidationError("Value cannot be negative.")


def validate_score(value: int) -> None:
    """
    Validate quiz score.
    """
    if not MIN_SCORE <= value <= MAX_SCORE:
        raise ValidationError(
            f"Score must be between {MIN_SCORE} and {MAX_SCORE}."
        )


def validate_not_blank(value: str) -> None:
    """
    Validate that text is not empty or only whitespace.
    """
    if not value.strip():
        raise ValidationError(
            "This field cannot be blank."
        )


def validate_image_size(image) -> None:
    """
    Validate uploaded image size.
    """
    if image.size > MAX_IMAGE_SIZE:
        raise ValidationError(
            f"Image size cannot exceed {MAX_IMAGE_SIZE // (1024 * 1024)} MB."
        )


def validate_image_extension(image) -> None:
    """
    Validate uploaded image extension.
    """
    extension = image.name.lower().rsplit(".", 1)[-1]

    extension = f".{extension}"

    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(
            f"Allowed formats: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
        )