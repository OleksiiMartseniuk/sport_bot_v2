from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from src.utils.unitofwork import SqlAlchemyUnitOfWork
from src.bot.callback.program import ProgramCallback, MenuLevels
from src.bot.keyboards.inline.program import ProgramKeyboard

from src.settings import MENU_IMAGE_FILE_ID


program_router = Router()


@program_router.message()
async def categories_view(message: Message, uow: SqlAlchemyUnitOfWork):
    categories_keyboard = await ProgramKeyboard.get_categories(uow=uow)
    await message.answer_photo(
        caption="Categories",
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
        caption="Categories",
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
    programs_keyboard = await ProgramKeyboard().get_program(
        uow=uow,
        category_id=callback_data.category,
    )
    await query.message.edit_caption(
        caption="Programs",
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
    days_keyboard = await ProgramKeyboard().get_program_days(
        uow=uow,
        category_id=callback_data.category,
        program_id=callback_data.program,
    )
    await query.message.edit_caption(
        caption="Days",
        reply_markup=days_keyboard,
    )

