import asyncio
import logging.config

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Update

from src.app.main import app
from src.bot.commands import set_commands
from src.bot.handlers.program import program_router
from src.bot.middlewares.registration import RegistrationUserMiddleware
from src.utils.unitofwork import SqlAlchemyUnitOfWork
from src.settings import (
    BOT_TOKEN,
    BASE_WEBHOOK_URL,
    WEBHOOK_SECRET,
    WEBHOOK_PATH_SECURITY,
    DEBUG,
    LOGGING_CONFIG,
)


WEBHOOK_PATH = f"/webhook/{WEBHOOK_PATH_SECURITY}"
WEBHOOK_URL = f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}"


def setup_bot() -> tuple[Bot, Dispatcher]:
    dp = Dispatcher()

    # Dependency
    dp["uow"] = SqlAlchemyUnitOfWork()

    # Middlewares
    dp.update.outer_middleware(RegistrationUserMiddleware())

    # Routers
    dp.include_routers(
        program_router,
    )

    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    return bot, dp


async def run_debug(bot: Bot, dp: Dispatcher):
    await set_commands(bot=bot)
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url:
        await bot.delete_webhook()
    await dp.start_polling(bot)


def main() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)
    bot, dp = setup_bot()
    if DEBUG:
        asyncio.run(run_debug(bot, dp))
    else:
        @app.on_event("startup")
        async def on_startup():
            await set_commands(bot)
            webhook_info = await bot.get_webhook_info()
            if webhook_info.url != WEBHOOK_URL:
                await bot.set_webhook(
                    url=WEBHOOK_URL,
                    secret_token=WEBHOOK_SECRET,
                )

        @app.on_event("shutdown")
        async def on_shutdown():
            await bot.session.close()

        @app.post(WEBHOOK_PATH)
        async def bot_webhook(update: dict):
            await dp.feed_webhook_update(bot=bot, update=Update(**update))

