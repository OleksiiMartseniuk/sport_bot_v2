import os
from typing import Any

from sqladmin import ModelView
from starlette.requests import Request

from src.database.models.history import HistoryExercise
from src.database.models.logger import StatusLog
from src.database.models.program import Category, Exercise, Program
from src.database.models.project_settings import ProjectSettings
from src.database.models.token import Token
from src.database.models.user import TelegramUser, User
from src.utils.unitofwork import SqlAlchemyUnitOfWork
from src.utils.utils import download_image


class StatusLogAdmin(ModelView, model=StatusLog):
    column_list = [
        StatusLog.id,
        StatusLog.logger_name,
        StatusLog.level,
        StatusLog.msg,
        StatusLog.created_at,
    ]
    column_sortable_list = [StatusLog.level]
    column_default_sort = ("created_at", True)


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


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.title]


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

    async def insert_model(self, request: Request, data: dict) -> Any:
        data["image"] = await download_image(url=data["image"])
        return await super().insert_model(request, data)

    async def update_model(self, request: Request, pk: str, data: dict) -> Any:
        uow = SqlAlchemyUnitOfWork()
        async with uow:
            exercise = await uow.exercise.get(id=int(pk))
            if exercise.image != data["image"] and "http" in data["image"]:
                data["image"] = await download_image(url=data["image"])
                if not exercise.image:
                    if os.path.isfile(exercise.image):
                        os.remove(exercise.image)
        return await super().update_model(request, pk, data)

    async def delete_model(self, request: Request, pk: Any) -> None:
        uow = SqlAlchemyUnitOfWork()
        async with uow:
            exercise = await uow.exercise.get(id=int(pk))
            if not exercise.image:
                if os.path.isfile(exercise.image):
                    os.remove(exercise.image)
        await super().delete_model(request, pk)


class HistoryExerciseAdmin(ModelView, model=HistoryExercise):
    column_list = [
        HistoryExercise.id,
        HistoryExercise.exercise,
        HistoryExercise.telegram_user,
        HistoryExercise.program,
    ]
    column_default_sort = ("created_at", True)


class ProjectSettingsAdmin(ModelView, model=ProjectSettings):
    column_list = [
        "id",
        "menu_image_telegram_id",
    ]


admin_view_models = [
    TokeAdmin,
    StatusLogAdmin,
    UserAdmin,
    TelegramUserAdmin,
    CategoryAdmin,
    ProgramAdmin,
    ExerciseAdmin,
    HistoryExerciseAdmin,
    ProjectSettingsAdmin,
]
