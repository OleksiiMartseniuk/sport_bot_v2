from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from src.settings import BOT_TOKEN
from src.bot.handlers.program import program_router
from src.bot.middlewares.registration import RegistrationUserMiddleware
from src.utils.unitofwork import SqlAlchemyUnitOfWork


async def main() -> None:
    dp = Dispatcher()
    dp["uow"] = SqlAlchemyUnitOfWork()

    dp.update.outer_middleware(RegistrationUserMiddleware())

    dp.include_routers(
        program_router,
    )

    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)

    await bot.set_my_commands(
        [
            BotCommand(
                command="program",
                description="Программа тренировок",
            ),
        ]
    )
    await dp.start_polling(bot)
