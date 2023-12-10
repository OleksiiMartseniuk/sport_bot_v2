import uvicorn

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, Update
from starlette.applications import Starlette

from starlette.requests import Request
from starlette.routing import Route

from src.settings import BOT_TOKEN
from src.bot.handlers.program import program_router
from src.bot.middlewares.registration import RegistrationUserMiddleware
from src.utils.unitofwork import SqlAlchemyUnitOfWork


# async def main() -> None:
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

# await bot.set_my_commands(
#     [
#         BotCommand(
#             command="program",
#             description="Программа тренировок",
#         ),
#     ]
# )
# await dp.start_polling(bot)
TUNNEL = "https://4m7s28h1-8000.euw.devtunnels.ms"
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"{TUNNEL}{WEBHOOK_PATH}"


# async def on_startup(bot: Bot) -> None:
#     await bot.set_webhook(
#         "https://4m7s28h1-8080.euw.devtunnels.ms:8080/webhook",
#     )
#
# dp.startup.register(on_startup)

from src.app.main import app
from starlette.endpoints import HTTPEndpoint



# async def webhook_response(request: Request):
#     update = Update.model_validate(await request.json(), context={"bot": bot})
#     return await dp.feed_raw_update(update)

# app.routes.append(Route("/webhook", endpoint=H))






async def webhook(request: Request):
    update = Update.model_validate(
        await request.json(),
        context={"bot": bot},
    )
    return await dp.feed_raw_update(update)

@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url == WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)

@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()

app.add_route(WEBHOOK_PATH, webhook, ["POST"])
# app.add_event_handler("startup", on_startup)
# app.add_event_handler("shutdown", on_shutdown)



uvicorn.run(
    app=app,
    host="0.0.0.0",
    port=8000
)
