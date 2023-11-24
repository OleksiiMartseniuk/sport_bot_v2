import uuid
from sqlalchemy import delete, insert

from src.database.models.token import Token
from src.utils.repository import SqlAlchemyRepository


class TokenRepository(SqlAlchemyRepository[Token]):
    model = Token

    async def get_or_create(self, user_id: int) -> Token:
        one = await self.get_or_none(user_id=user_id)
        if one:
            return one
        else:
            stmt = insert(self.model).values(
                user_id=user_id,
                token=uuid.uuid4().hex,
            ).returning(self.model)
            res = await self.session.execute(stmt)
            return res.scalar_one()

    async def delete(self, token: str) -> None:
        stmt = (
            delete(self.model).where(self.model.token == token)
            .returning(self.model.id)
        )
        await self.session.execute(stmt)
