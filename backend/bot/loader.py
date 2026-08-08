"""
Bot loader.

Initializes the main Aiogram bot and dispatcher instances.
"""

from __future__ import annotations

from aiogram import Bot, Dispatcher

from bot.config import config


bot = Bot(
    token=config.token,
)

dp = Dispatcher()