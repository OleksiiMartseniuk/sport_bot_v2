from aiogram import F, Router
from aiogram.types import Message

from src.bot.keyboards.reply.profile import ProfileSettingKeyboard
from src.utils.unitofwork import SqlAlchemyUnitOfWork

profile_router = Router()


@profile_router.message(F.text.startswith("/profile"))
async def profile_setting_view(message: Message, uow: SqlAlchemyUnitOfWork):
    keyboard_menu = await ProfileSettingKeyboard.get_menu_setting(
        uow=uow,
        telegram_id=message.from_user.id,
    )
    await message.answer("Настройки профиля", reply_markup=keyboard_menu)


@profile_router.message(F.text.startswith("/start"))
async def is_schedule_view(message: Message, uow: SqlAlchemyUnitOfWork):
    keyboard_menu = await ProfileSettingKeyboard.get_menu_setting(
        uow=uow,
        telegram_id=message.from_user.id,
    )
    await message.answer("Настройки профиля", reply_markup=keyboard_menu)
