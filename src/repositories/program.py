from src.database.models.program import Category, Program, Exercise
from src.utils.repository import SqlAlchemyRepository


class CategoryRepository(SqlAlchemyRepository):
    model = Category


class ExerciseRepository(SqlAlchemyRepository):
    model = Exercise


class ProgramRepository(SqlAlchemyRepository):
    model = Program
