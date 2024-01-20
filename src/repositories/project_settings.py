from aiogram.types import InputMediaPhoto, FSInputFile

from src.database.models.project_settings import ProjectSettings
from src.utils.repository import SqlAlchemyRepository


class ProjectSettingsError(Exception):
    pass


class ExistsProjectSettingsError(ProjectSettingsError):
    pass


class ProjectSettingsRepository(SqlAlchemyRepository[ProjectSettings]):
    model = ProjectSettings

    async def __check_exists(self):
        is_exists = await self.exists()
        if is_exists:
            raise ExistsProjectSettingsError()

    async def create(self, data: dict) -> int:
        await self.__check_exists()
        return await super().create(data)

    async def get_image_telegram(
        self,
        caption: str | None = None,
    ) -> InputMediaPhoto:
        project_settings = await self.get()
        if project_settings.menu_image_telegram_id:
            return InputMediaPhoto(
                media=project_settings.menu_image_telegram_id,
                caption=caption,
            )
        else:
            return InputMediaPhoto(
                media=FSInputFile(path=project_settings.menu_image_path),
                caption=caption,
            )
