from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.utils.unitofwork import SqlAlchemyUnitOfWork


class ProfileSettingKeyboard:
    @staticmethod
    async def get_menu_setting(
        uow: SqlAlchemyUnitOfWork, telegram_id: int
    ) -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        async with uow:
            telegram_user = await uow.telegram_user.get(telegram_id=telegram_id)
            massage = (
                "Отключить расписание"
                if telegram_user.is_schedule
                else "Включить расписание"
            )
            builder.row(KeyboardButton(text=massage))
        return builder.as_markup(resize_keyboard=True)
