"""
Bot configuration.

Loads environment variables required by the Telegram bot.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


# Load .env from the backend directory.
load_dotenv()


@dataclass(frozen=True)
class BotConfig:
    """
    Telegram bot configuration.
    """

    token: str
    api_base_url: str
    api_token: str


def _get_required_env(name: str) -> str:
    """
    Return a required environment variable.

    Raises:
        RuntimeError: If the variable is missing or empty.
    """

    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Required environment variable '{name}' is not set."
        )

    return value


config = BotConfig(
    token=_get_required_env("BOT_TOKEN"),
    api_base_url=os.getenv(
        "API_BASE_URL",
        "http://127.0.0.1:8000/api/",
    ),
    api_token=_get_required_env("BOT_API_TOKEN"),
)