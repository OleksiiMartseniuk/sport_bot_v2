from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.utils.unitofwork import SqlAlchemyUnitOfWork
from src.utils.utils import WeekDict, Week
from src.bot.callback.program import ProgramCallback, MenuLevels
from src.database.models.program import Exercise


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
                        menu_level=MenuLevels.day,
                        category=category_id,
                        program=program.id,
                        day=7,
                        exercise=0,
                    )
                )
            button_back = self.__get_button_back(
                program_callback=ProgramCallback(
                    menu_level=MenuLevels.category,
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

    async def get_program_days(
        self,
        uow: SqlAlchemyUnitOfWork,
        category_id: int,
        program_id: int,
    ) -> InlineKeyboardMarkup:
        async with uow:
            days_db = await uow.exercise.get_program_days(
                program_id=program_id,
            )
            builder = InlineKeyboardBuilder()
            for day in days_db:
                builder.button(
                    text=WeekDict.get(day.value, "Undefined"),
                    callback_data=ProgramCallback(
                        menu_level=MenuLevels.exercises,
                        category=category_id,
                        program=program_id,
                        day=day.value,
                        exercise=0,
                    )
                )
            button_back = self.__get_button_back(
                program_callback=ProgramCallback(
                    menu_level=MenuLevels.program,
                    category=category_id,
                    program=program_id,
                    day=7,
                    exercise=0,
                )
            )
            builder.adjust(3)
            builder.attach(InlineKeyboardBuilder.from_markup(button_back))
            return builder.as_markup()

    async def get_exercises(
        self,
        uow: SqlAlchemyUnitOfWork,
        category_id: int,
        program_id: int,
        day: int,
    ) -> InlineKeyboardMarkup:
        async with uow:
            exercises = await uow.exercise.all(
                program_id=program_id,
                day=Week(day),
            )
            builder = InlineKeyboardBuilder()
            for exercise in exercises:
                builder.button(
                    text=exercise.title,
                    callback_data=ProgramCallback(
                        menu_level=MenuLevels.exercise,
                        category=category_id,
                        program=program_id,
                        day=day,
                        exercise=exercise.id,
                    )
                )
            button_back = self.__get_button_back(
                program_callback=ProgramCallback(
                    menu_level=MenuLevels.day,
                    category=category_id,
                    program=program_id,
                    day=7,
                    exercise=0,
                )
            )
            builder.adjust(1)
            builder.attach(InlineKeyboardBuilder.from_markup(button_back))
            return builder.as_markup()

    async def get_exercise(
        self,
        uow: SqlAlchemyUnitOfWork,
        category_id: int,
        program_id: int,
        day: int,
        exercise_id: int,
        telegram_id: int,
    ):
        async with uow:
            exercises = await uow.exercise.get(id=exercise_id)
            user = await uow.user.get(telegram_id=telegram_id)
            history_count = await uow.history_exercise.count(
                user_id=user.id,
                program_id=program_id,
                exercise_id=exercise_id,
            )
            text = self.get_exercise_description(
                exercises=exercises,
                current_approach=history_count,
            )
            if user.program_id == program_id:
                pass
            else:
                pass

        return text

    @staticmethod
    def get_exercise_description(
        exercises: Exercise,
        current_approach: int | None,
    ):
        text = (
            f"<b>{exercises.title}</b>\n\n"
            f"Количество повторений: "
            f"<b>{exercises.number_of_repetitions}</b>\n"
        )
        if exercises.rest:
            text += f"Отдых между подходами: <b>{exercises.rest / 60} м</b>\n"
        if current_approach:
            text += (
                f"Количество подходов: <b>{exercises.number_of_approaches}</b>"
                f"/<b>{current_approach}</b>\n"
            )
        else:
            text += (
                f"Количество подходов: "
                f"<b>{exercises.number_of_approaches}</b>\n"
            )
        return text
