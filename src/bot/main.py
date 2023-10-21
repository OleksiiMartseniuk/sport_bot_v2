from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from src.settings import BOT_TOKEN
from src.bot.handlers.program import program_router
from src.utils.unitofwork import SqlAlchemyUnitOfWork


async def main() -> None:
    dp = Dispatcher()
    dp["uow"] = SqlAlchemyUnitOfWork()

    dp.include_routers(
        program_router,
    )

    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)
