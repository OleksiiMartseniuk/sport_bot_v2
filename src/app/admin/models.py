from sqladmin import ModelView

from src.database.models.user import TelegramUser, User
from src.database.models.token import Token
from src.database.models.program import Program, Exercise
from src.database.models.history import HistoryExercise


class TokeAdmin(ModelView, model=Token):
    column_list = [Token.id, Token.user_id, Token.user]


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.username,
        User.is_staff,
        User.is_superuser,
    ]
    form_excluded_columns = [User.password]


class TelegramUserAdmin(ModelView, model=TelegramUser):
    column_list = [
        TelegramUser.id,
        TelegramUser.username,
        TelegramUser.telegram_id,
        TelegramUser.program,
        TelegramUser.created_at,
    ]


class ProgramAdmin(ModelView, model=Program):
    column_list = [Program.id, Program.title]


class ExerciseAdmin(ModelView, model=Exercise):
    column_list = [
        Exercise.id,
        Exercise.title,
        Exercise.day,
        Exercise.program,
    ]
    column_sortable_list = [Exercise.day]
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
    TokeAdmin,
    UserAdmin,
    TelegramUserAdmin,
    ProgramAdmin,
    ExerciseAdmin,
    HistoryExerciseAdmin,
]
