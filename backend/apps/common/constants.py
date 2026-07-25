"""
Global project constants.

All reusable constant values should be defined here.
"""

from __future__ import annotations

PROJECT_NAME: str = "AI Education Bot"

DEFAULT_LANGUAGE: str = "uz"

DEFAULT_PAGE_SIZE: int = 20

MAX_PAGE_SIZE: int = 100

MAX_IMAGE_SIZE: int = 5 * 1024 * 1024  # 5 MB

ALLOWED_IMAGE_EXTENSIONS: tuple[str, ...] = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
)

MAX_TITLE_LENGTH: int = 255

MAX_DESCRIPTION_LENGTH: int = 2000

MIN_SCORE: int = 0

MAX_SCORE: int = 100

DEFAULT_XP_REWARD: int = 10