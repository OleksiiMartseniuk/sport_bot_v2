from src.database.models.history import HistoryExercise
from src.utils.repository import SqlAlchemyRepository


class HistoryExerciseRepository(SqlAlchemyRepository):
    model = HistoryExercise
