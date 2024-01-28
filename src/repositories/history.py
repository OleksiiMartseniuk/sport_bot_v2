from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from src.database.models.history import HistoryExercise
from src.database.models.program import Program
from src.utils.repository import SqlAlchemyRepository


class HistoryExerciseRepository(SqlAlchemyRepository[HistoryExercise]):
    model = HistoryExercise

    async def get_count_history_today(self, **filters) -> int:
        stmt = (
            select(func.count(self.model.id))
            .filter_by(**filters)
            .where(func.date(self.model.created_at) == datetime.utcnow().date())
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get_statistics(self, telegram_user_id: int, **filters):
        stmt = (
            select(self.model)
            .options(
                selectinload(self.model.exercise),
                selectinload(self.model.program).selectinload(Program.category),
            )
            .filter_by(**filters)
            .where(self.model.telegram_user_id == telegram_user_id)
        )
        res = await self.session.execute(stmt)
        return res.scalars().all()
