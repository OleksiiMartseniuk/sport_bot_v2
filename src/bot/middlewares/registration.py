from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from src.utils.unitofwork import SqlAlchemyUnitOfWork


class RegistrationUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        await self.registration_user(
            user=data["event_from_user"],
            uow=data["uow"],
        )
        return await handler(event, data)

    @staticmethod
    async def registration_user(user: User, uow: SqlAlchemyUnitOfWork):
        async with uow:
            await uow.user.get_or_create(telegram_id=user.id)
            await uow.commit()
