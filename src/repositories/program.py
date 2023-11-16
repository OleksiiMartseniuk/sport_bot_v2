from sqlalchemy import select

from src.database.models.program import Category, Program, Exercise
from src.utils.repository import SqlAlchemyRepository
from src.utils.utils import Week


class CategoryRepository(SqlAlchemyRepository[Category]):
    model = Category


class ExerciseRepository(SqlAlchemyRepository[Exercise]):
    model = Exercise

    async def get_program_days(self, program_id: int) -> list[Week]:
        stmt = (
            select(self.model.day)
            .where(self.model.program_id == program_id)
            .order_by(self.model.day)
            .distinct()
        )
        res = await self.session.execute(stmt)
        return res.scalars().all()


class ProgramRepository(SqlAlchemyRepository[Program]):
    model = Program
