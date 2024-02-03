import logging

from aiogram import Bot
from aiogram.types import BotCommand

logger = logging.getLogger("db")


async def set_commands(bot: Bot):
    try:
        await bot.set_my_commands(
            [
                BotCommand(
                    command="program",
                    description="Программа тренировок",
                ),
                BotCommand(
                    command="profile",
                    description="Настройки профиля",
                ),
            ]
        )
    except Exception as ex:
        logger.error("Error setting commands", exc_info=ex)
