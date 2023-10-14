from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete


class AbstractRepository(ABC):
    @abstractmethod
    async def create(self, data: dict):
        ...

    @abstractmethod
    async def get(self, **filters):
        ...

    @abstractmethod
    async def update(self, data: dict, **fields):
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

    async def get(self, **filters) -> model:
        stmt = select(self.model).filter_by(**filters)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def update(self, data: dict, **filters) -> int:
        stmt = (
            update(self.model).filter_by(**filters)
            .values(**data).returning(self.model.id)
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

    async def exists(self, **filters) -> bool:
        exists_criteria = (
            select(self.model).filter_by(**filters).exists().select()
        )
        res = await self.session.execute(exists_criteria)
        return res.scalar()
