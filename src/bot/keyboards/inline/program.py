from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.utils.unitofwork import SqlAlchemyUnitOfWork
from src.bot.callback.program import ProgramCallback, MenuLevels


class ProgramKeyboard:
    @staticmethod
    async def get_categories(
        uow: SqlAlchemyUnitOfWork,
    ) -> InlineKeyboardMarkup:
        async with uow:
            categories = await uow.category.all()
            builder = InlineKeyboardBuilder()
            for category in categories:
                builder.button(
                    text=category.title,
                    callback_data=ProgramCallback(
                        menu_level=MenuLevels.program,
                        category=category.id,
                        program=0,
                        day=7,
                        exercise=0,
                    ),
                )
        return builder.as_markup()

    async def get_program(
        self,
        uow: SqlAlchemyUnitOfWork,
        category_id: int,
    ) -> InlineKeyboardMarkup:
        async with (uow):
            builder = InlineKeyboardBuilder()
            programs = await uow.program.all(category_id=category_id)
            for program in programs:
                builder.button(
                    text=program.title,
                    callback_data=ProgramCallback(
                        menu_level=MenuLevels.program,
                        category=category_id,
                        program=program.id,
                        day=7,
                        exercise=0,
                    )
                )
            button_back = self.__get_button_back(
                program_callback=ProgramCallback(
                    menu_level=MenuLevels.program,
                    category=category_id,
                    program=program.id,
                    day=7,
                    exercise=0,
                )
            )
            builder.attach(InlineKeyboardBuilder.from_markup(button_back))
        return builder.as_markup()

    @staticmethod
    def __get_button_back(
        program_callback: ProgramCallback
    ) -> InlineKeyboardMarkup:
        button_back = [
            [
                InlineKeyboardButton(
                    text="Back",
                    callback_data=program_callback.pack()
                )
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=button_back)
