from aiogram import Router
from aiogram.types import Message


program_router = Router()


@program_router.message()
async def get_category(message: Message):
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")
