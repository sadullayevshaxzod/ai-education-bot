"""
Reusable utility functions.

Only project-wide helper functions should be placed here.
"""

from __future__ import annotations

import secrets
import string


def generate_numeric_code(length: int = 6) -> str:
    """
    Generate a secure random numeric code.

    Args:
        length: Number of digits.

    Returns:
        Random numeric string.

    Example:
        >>> generate_numeric_code()
        '483921'
    """
    if length <= 0:
        raise ValueError("Code length must be greater than zero.")

    return "".join(
        secrets.choice(string.digits)
        for _ in range(length)
    )