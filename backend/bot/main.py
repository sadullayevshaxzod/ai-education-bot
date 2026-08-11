"""
Telegram bot entry point.
"""

from __future__ import annotations

import asyncio
import logging

from bot.loader import bot, dp


async def main() -> None:
    """
    Start the Telegram bot.
    """

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
    )

    await dp.start_polling(
        bot,
    )


if __name__ == "__main__":
    asyncio.run(main())