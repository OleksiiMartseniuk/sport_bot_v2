from datetime import datetime

from sqlalchemy import select, func

from src.database.models.history import HistoryExercise
from src.utils.repository import SqlAlchemyRepository


class HistoryExerciseRepository(SqlAlchemyRepository[HistoryExercise]):
    model = HistoryExercise

    async def get_count_history_today(self, **filters) -> int:
        stmt = select(func.count(self.model.id)).filter_by(**filters).where(
            func.date(self.model.created_at) == datetime.utcnow().date()
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()
