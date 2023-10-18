from src.database.models.program import Category, Program, Exercise
from src.utils.repository import SqlAlchemyRepository


class CategoryRepository(SqlAlchemyRepository[Category]):
    model = Category


class ExerciseRepository(SqlAlchemyRepository[Exercise]):
    model = Exercise


class ProgramRepository(SqlAlchemyRepository[Program]):
    model = Program
