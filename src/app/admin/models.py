from sqladmin import ModelView

from src.database.models.user import TelegramUser
from src.database.models.program import Program, Exercise
from src.database.models.history import HistoryExercise


class UserAdmin(ModelView, model=TelegramUser):
    column_list = [TelegramUser.id, TelegramUser.telegram_id]


class ProgramAdmin(ModelView, model=Program):
    column_list = [Program.id, Program.title]


class ExerciseAdmin(ModelView, model=Exercise):
    column_list = [
        Exercise.id,
        Exercise.title,
        Exercise.program,
    ]
    column_searchable_list = [Exercise.program_id]


class HistoryExerciseAdmin(ModelView, model=HistoryExercise):
    column_list = [
        HistoryExercise.id,
        HistoryExercise.exercise,
        HistoryExercise.telegram_user,
        HistoryExercise.program,
    ]
    column_default_sort = ("created_at", True)


admin_view_models = [
    UserAdmin,
    ProgramAdmin,
    ExerciseAdmin,
    HistoryExerciseAdmin,
]
