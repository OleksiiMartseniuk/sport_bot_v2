from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from src.utils.unitofwork import SqlAlchemyUnitOfWork
from src.bot.callback.program import ProgramCallback, MenuLevels
from src.bot.keyboards.inline.program import ProgramKeyboard

from src.settings import MENU_IMAGE_FILE_ID


program_router = Router()


@program_router.message(Command("program"))
async def categories_view(message: Message, uow: SqlAlchemyUnitOfWork):
    categories_keyboard = await ProgramKeyboard.get_categories(uow=uow)
    await message.answer_photo(
        caption="Категории",
        photo=MENU_IMAGE_FILE_ID,
        reply_markup=categories_keyboard,
    )


@program_router.callback_query(
    ProgramCallback.filter(F.menu_level == MenuLevels.category)
)
async def categories_callback_view(
    query: CallbackQuery,
    uow: SqlAlchemyUnitOfWork,
):
    categories_keyboard = await ProgramKeyboard.get_categories(uow=uow)
    await query.message.edit_caption(
        caption="Категории",
        reply_markup=categories_keyboard,
    )


@program_router.callback_query(
    ProgramCallback.filter(F.menu_level == MenuLevels.program)
)
async def programs_view(
    query: CallbackQuery,
    callback_data: ProgramCallback,
    uow: SqlAlchemyUnitOfWork,
):
    programs_keyboard, text = await ProgramKeyboard().get_program(
        uow=uow,
        category_id=callback_data.category,
        subscription=callback_data.subscription,
        telegram_id=query.from_user.id,
    )
    await query.message.edit_caption(
        caption=text,
        reply_markup=programs_keyboard,
    )


@program_router.callback_query(
    ProgramCallback.filter(F.menu_level == MenuLevels.day)
)
async def program_days_view(
    query: CallbackQuery,
    callback_data: ProgramCallback,
    uow: SqlAlchemyUnitOfWork,
):
    days_keyboard, text = await ProgramKeyboard().get_program_days(
        uow=uow,
        category_id=callback_data.category,
        program_id=callback_data.program,
    )
    await query.message.edit_caption(
        caption=text,
        reply_markup=days_keyboard,
    )


@program_router.callback_query(
    ProgramCallback.filter(F.menu_level == MenuLevels.exercises)
)
async def exercises_view(
    query: CallbackQuery,
    callback_data: ProgramCallback,
    uow: SqlAlchemyUnitOfWork,
):
    exercises_keyboard, media = await ProgramKeyboard().get_exercises(
        uow=uow,
        category_id=callback_data.category,
        program_id=callback_data.program,
        day=callback_data.day,
    )
    await query.message.edit_media(
        media=media,
        reply_markup=exercises_keyboard,
    )


@program_router.callback_query(
    ProgramCallback.filter(F.menu_level == MenuLevels.exercise)
)
async def exercise_view(
    query: CallbackQuery,
    callback_data: ProgramCallback,
    uow: SqlAlchemyUnitOfWork,
):
    keyboard, media, created_image = await ProgramKeyboard().get_exercise(
        uow=uow,
        telegram_id=query.from_user.id,
        callback=callback_data,
        today=query.message.date,
    )

    if created_image is False:
        response = await query.message.edit_media(
            media=media,
            reply_markup=keyboard,
        )
        async with uow:
            await uow.exercise.update(
                data={"telegram_image_id": response.photo[-1].file_id},
                id=callback_data.exercise,
            )
            await uow.commit()
    else:
        await query.message.edit_media(
            media=media,
            reply_markup=keyboard,
        )
