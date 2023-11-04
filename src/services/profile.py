import logging

from src.utils.unitofwork import SqlAlchemyUnitOfWork

logger = logging.getLogger(__name__)


class ProfileService:
    @staticmethod
    async def subscribe_to_program(
        program_id: int,
        uow_transaction: SqlAlchemyUnitOfWork,
        **user_filter
    ) -> None:
        await uow_transaction.user.update(
            **user_filter,
            data={"program_id": program_id},
        )
        await uow_transaction.commit()

    @staticmethod
    async def unsubscribe_to_program(
        uow_transaction: SqlAlchemyUnitOfWork,
        **user_filter
    ) -> None:
        await uow_transaction.user.update(
            **user_filter,
            data={"program_id": None},
        )
        await uow_transaction.commit()
