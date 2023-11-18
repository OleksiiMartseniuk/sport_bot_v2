from sqlalchemy import update

from src.database.models.user import TelegramUser
from src.utils.repository import SqlAlchemyRepository


class TelegramUserRepository(SqlAlchemyRepository[TelegramUser]):
    model = TelegramUser

    async def subscribe_to_program(
        self,
        program_id: int,
        **user_filter,
    ) -> None:
        stmt = (
            update(self.model).filter_by(**user_filter)
            .values({"program_id": program_id}).returning(self.model.id)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def unsubscribe_to_program(self, **user_filter) -> None:
        stmt = (
            update(self.model).filter_by(**user_filter)
            .values({"program_id": None}).returning(self.model.id)
        )
        await self.session.execute(stmt)
        await self.session.commit()
