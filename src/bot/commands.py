from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    await bot.set_my_commands(
        [
            BotCommand(
                command="program",
                description="Программа тренировок",
            ),
        ]
    )
