from src.database.models.project_settings import ProjectSettings
from src.utils.repository import SqlAlchemyRepository


class ProjectSettingsRepository(SqlAlchemyRepository[ProjectSettings]):
    model = ProjectSettings

    async def __check_exists(self):
        is_exists = await self.exists()
        if is_exists:
            raise ValueError("ProjectSettings exists")

    async def create(self, data: dict) -> int:
        await self.__check_exists()
        return await super().create(data)
