from abc import ABC, abstractmethod

from src.database.base import async_session
from src.repositories.program import (
    CategoryRepository,
    ProgramRepository,
    ExerciseRepository,
)
from src.repositories.telegram_user import TelegramUserRepository
from src.repositories.user import UserRepository
from src.repositories.history import HistoryExerciseRepository
from src.repositories.token import TokenRepository
from src.repositories.project_settings import ProjectSettingsRepository


class UnitOfWork(ABC):
    category: CategoryRepository
    program: ProgramRepository
    exercise: ExerciseRepository
    telegram_user: TelegramUserRepository
    history_exercise: HistoryExerciseRepository
    token: TokenRepository
    user: UserRepository
    project_settings: ProjectSettingsRepository

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args, **kwargs):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self):
        self.session_factory = async_session

    async def __aenter__(self):
        self.session = self.session_factory()

        self.category = CategoryRepository(self.session)
        self.program = ProgramRepository(self.session)
        self.exercise = ExerciseRepository(self.session)
        self.telegram_user = TelegramUserRepository(self.session)
        self.history_exercise = HistoryExerciseRepository(self.session)
        self.token = TokenRepository(self.session)
        self.user = UserRepository(self.session)
        self.project_settings = ProjectSettingsRepository(self.session)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
