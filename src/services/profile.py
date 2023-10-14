import logging

from src.utils.unitofwork import SqlAlchemyUnitOfWork

logger = logging.getLogger(__name__)


class ProfileService:
    def __init__(
        self,
        uow: SqlAlchemyUnitOfWork,
        **user_filter,
    ):
        if not user_filter:
            raise ValueError("No data to get user")
        self.user_filter = user_filter
        self.uow = uow

    async def subscribe_to_program(self, program_id: int) -> None:
        async with self.uow:
            await self.uow.user.update(
                **self.user_filter,
                data={"program_id": program_id},
            )
            await self.uow.commit()

    async def unsubscribe_to_program(self) -> None:
        async with self.uow:
            await self.uow.user.update(
                **self.user_filter,
                data={"program_id": None},
            )
            await self.uow.commit()
