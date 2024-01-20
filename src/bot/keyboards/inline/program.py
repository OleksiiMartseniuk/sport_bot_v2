from datetime import datetime

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile,
    InputMediaPhoto,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.utils.unitofwork import SqlAlchemyUnitOfWork
from src.utils.utils import WeekDict, Week
from src.bot.callback.program import ProgramCallback, MenuLevels
from src.database.models.program import Exercise
from src.services.history import HistoryService


class ProgramKeyboard:
    @staticmethod
    async def get_categories(
        uow: SqlAlchemyUnitOfWork,
    ) -> tuple[InlineKeyboardMarkup, str | FSInputFile]:
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
            builder.adjust(1)
            is_create, project_settings = (
                await uow.project_settings.get_or_create()
            )
            if is_create:
                await uow.commit()
            if project_settings.menu_image_telegram_id:
                photo = project_settings.menu_image_telegram_id
            else:
                photo = FSInputFile(path=project_settings.menu_image_path)
        return builder.as_markup(), photo

    async def get_program(
        self,
        uow: SqlAlchemyUnitOfWork,
        category_id: int,
        subscription: int,
        telegram_id: int,
    ) -> tuple[InlineKeyboardMarkup, str]:
        subscribe = "Подписаться"
        unsubscribe = "Отписаться"
        async with (uow):
            builder = InlineKeyboardBuilder()
            await self.__subscription(
                subscription=subscription,
                telegram_id=telegram_id,
                uow=uow,
            )
            user = await uow.telegram_user.get(telegram_id=telegram_id)
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
                text = (
                    unsubscribe if program.id == user.program_id else subscribe
                )
                builder.button(
                    text=text,
                    callback_data=ProgramCallback(
                        menu_level=MenuLevels.program,
                        category=category_id,
                        program=0,
                        subscription=program.id,
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
            builder.adjust(2)
            builder.attach(InlineKeyboardBuilder.from_markup(button_back))
            category = await uow.category.get(id=category_id)
            return builder.as_markup(), category.title

    @staticmethod
    async def __subscription(
        subscription: int,
        telegram_id: int,
        uow: SqlAlchemyUnitOfWork,
    ) -> None:
        if subscription != 0:
            user = await uow.telegram_user.get(telegram_id=telegram_id)
            if subscription == user.program_id:
                await uow.telegram_user.unsubscribe_to_program(id=user.id)
            else:
                await uow.telegram_user.subscribe_to_program(
                    program_id=subscription,
                    id=user.id,
                )

    @staticmethod
    def __get_button_back(
        program_callback: ProgramCallback
    ) -> InlineKeyboardMarkup:
        button_back = [
            [
                InlineKeyboardButton(
                    text="Назад",
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
    ) -> tuple[InlineKeyboardMarkup, str]:
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
            builder.adjust(2)
            builder.attach(InlineKeyboardBuilder.from_markup(button_back))
            program = await uow.program.get(id=program_id)
            return builder.as_markup(), program.title

    async def get_exercises(
        self,
        uow: SqlAlchemyUnitOfWork,
        category_id: int,
        program_id: int,
        day: int,
    ) -> tuple[InlineKeyboardMarkup, InputMediaPhoto]:
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
            media = await uow.project_settings.get_image_telegram(
                caption=WeekDict[day],
            )
            return builder.as_markup(), media

    async def get_exercise(
        self,
        uow: SqlAlchemyUnitOfWork,
        callback: ProgramCallback,
        telegram_id: int,
        today: datetime,
    ) -> tuple[InlineKeyboardMarkup, InputMediaPhoto, bool]:
        builder = InlineKeyboardBuilder()
        calculate_result = self.calculate(
            action=callback.action,
            value=callback.value,
        )
        callback_data = ProgramCallback(
            category=callback.category,
            menu_level=MenuLevels.exercise,
            program=callback.program,
            day=callback.day,
            exercise=callback.exercise,
            value=calculate_result,
        )
        async with uow:
            user = await uow.telegram_user.get(telegram_id=telegram_id)
            exercise = await uow.exercise.get(id=callback.exercise)
            history_count = await uow.history_exercise.get_count_history_today(
                telegram_user_id=user.id,
                program_id=callback.program,
                exercise_id=callback.exercise,
            )
            if callback.confirm:
                await HistoryService.create_history_exercise(
                    uow=uow,
                    exercise_id=callback.exercise,
                    telegram_user_id=user.id,
                    program_id=callback.program,
                    approach=history_count + 1,
                    number_of_repetitions=callback.value,
                )
                callback_data.value, calculate_result = 0, 0
                history_count = (
                    await uow.history_exercise.get_count_history_today(
                        telegram_user_id=user.id,
                        program_id=callback.program,
                        exercise_id=callback.exercise,
                    )
                )

            text = self.get_exercise_description(
                exercise=exercise,
                current_approach=history_count,
            )

            if (
                user.program_id == callback.program and
                history_count < exercise.number_of_approaches and
                (user.is_schedule or today.weekday() == callback.day)
            ):
                text += (
                    f"{'=' * 20}"
                    f"\nКоличество сделанных повторений: {calculate_result}\n"
                )
                increment_callback_data = callback_data.model_copy()
                decrement_callback_data = callback_data.model_copy()
                confirm_callback_data = callback_data.model_copy()
                full_value_callback_data = callback_data.model_copy()
                full_value_callback_data.value = exercise.number_of_repetitions
                confirm_callback_data.confirm = True
                increment_callback_data.action = "+1"
                decrement_callback_data.action = "-1"
                buttons = [
                    [
                        InlineKeyboardButton(
                            text=increment_callback_data.action,
                            callback_data=increment_callback_data.pack(),
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="Подтвердить",
                            callback_data=confirm_callback_data.pack()
                        ),
                    ]
                ]
                if calculate_result > 0:
                    buttons[0].append(
                        InlineKeyboardButton(
                            text=decrement_callback_data.action,
                            callback_data=decrement_callback_data.pack(),
                        ),
                    )
                if self.is_percent_repetitions(
                    value=calculate_result,
                    repetitions=exercise.number_of_repetitions,
                ):
                    buttons[0].append(
                        InlineKeyboardButton(
                            text=f"Set {full_value_callback_data.value}",
                            callback_data=full_value_callback_data.pack(),
                        ),
                    )
                keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
                builder.attach(InlineKeyboardBuilder.from_markup(keyboard))

            button_back = self.__get_button_back(
                program_callback=ProgramCallback(
                    menu_level=MenuLevels.exercises,
                    category=callback.category,
                    program=callback.program,
                    day=callback.day,
                    exercise=callback.exercise,
                )
            )
            builder.attach(InlineKeyboardBuilder.from_markup(button_back))
            media, created_image = await self.get_media(
                exercise=exercise,
                text=text,
                uow=uow,
            )
        return builder.as_markup(), media, created_image

    @staticmethod
    def get_exercise_description(
        exercise: Exercise,
        current_approach: int | None,
    ):
        text = (
            f"<b>{exercise.title}</b>\n\n"
            f"Количество повторений: "
            f"<b>{exercise.number_of_repetitions}</b>\n"
        )
        if exercise.rest:
            text += f"Отдых между подходами: <b>{exercise.rest / 60} м</b>\n"
        if current_approach:
            text += (
                f"Количество подходов: <b>{exercise.number_of_approaches}</b>"
                f"/<b>{current_approach}</b>\n"
            )
        else:
            text += (
                f"Количество подходов: "
                f"<b>{exercise.number_of_approaches}</b>\n"
            )
        return text

    @staticmethod
    async def get_media(
        exercise: Exercise,
        text: str,
        uow: SqlAlchemyUnitOfWork,
    ) -> tuple[InputMediaPhoto, bool]:
        if exercise.telegram_image_id:
            media = InputMediaPhoto(
                media=exercise.telegram_image_id,
                caption=text,
            )
            return media, True
        elif exercise.telegram_image_id is None and exercise.image:
            media = InputMediaPhoto(
                media=FSInputFile(path=exercise.image),
                caption=text,
            )
            return media, False
        else:
            media = await uow.project_settings.get_image_telegram(caption=text)
            return media, True

    @staticmethod
    def calculate(action: str | None = None, value: int = 0) -> int:
        if action == "-1":
            if value > 0:
                value = value - 1
        elif action == "+1":
            value = value + 1
        return value

    @staticmethod
    def is_percent_repetitions(value: int, repetitions: int) -> bool:
        percent = 80
        return int((value / repetitions) * 100) < percent
