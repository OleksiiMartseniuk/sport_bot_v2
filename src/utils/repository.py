from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete


class AbstractRepository(ABC):
    @abstractmethod
    async def create(self, data: dict):
        ...

    @abstractmethod
    async def get(self, id: int):
        ...

    @abstractmethod
    async def update(self, id: int):
        ...

    @abstractmethod
    async def delete(self, id: int):
        ...


class SqlAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get(self, id: int) -> model:
        stmt = select(self.model).where(self.model.id == id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def update(self, id: int, **fields) -> int:
        stmt = (
            update(self.model).where(self.model.id == id)
            .values(**fields).returning(self.model.id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete(self, id: int) -> int:
        stmt = (
            delete(self.model).where(self.model.id == id)
            .returning(self.model.id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get_or_create(self, **filter) -> model:
        stmt = select(self.model).filter_by(**filter)
        res = await self.session.execute(stmt)
        one = res.scalar_one_or_none()
        if one:
            return one
        else:
            stmt = insert(self.model).values(**filter).returning(self.model)
            res = await self.session.execute(stmt)
            return res.scalar_one()
