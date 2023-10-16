import csv
import logging
import uuid

import httpx
import aiofiles

from src.utils.unitofwork import SqlAlchemyUnitOfWork
from src.schemas.import_data import File
from src.settings import IMAGES_DIR


class ImportDataService:
    def __init__(self, logger: logging.Logger = logging.getLogger(__name__)):
        self.data = []
        self.uow = SqlAlchemyUnitOfWork()
        self.logger = logger

    def __get_data_file(self, path: str) -> None:
        with open(path) as csvfile:
            reader = csv.DictReader(csvfile)

            fields_list = list(reader.fieldnames)
            required_fields_list = list(File.model_fields.keys())
            if fields_list.sort() != required_fields_list.sort():
                raise ValueError("Not required fields")

            for row in reader:
                row_data = {key: data.strip() for key, data in row.items()}
                self.data.append(row_data)

    async def import_file(self, path: str) -> None:
        self.__get_data_file(path=path)

        for idx, item in enumerate(self.data, 1):
            try:
                obj = File(**item)
                async with self.uow:
                    category = await self.uow.category.get_or_create(
                        title=obj.category
                    )
                    program = await self.uow.program.get_or_create(
                        title=obj.program,
                        category_id=category.id,
                    )
                    exercise = await self.uow.exercise.get_or_create(
                        program_id=program.id,
                        **obj.get_fields_exercise(),
                    )
                    if exercise.image is None:
                        image_path = await self.__download_image(
                            url=obj.exercise_image_url,
                        )
                        if image_path:
                            await self.uow.exercise.update(
                                id=exercise.id,
                                data={"image": image_path},
                            )
                    await self.uow.commit()
            except Exception as ex:
                self.logger.error(f"Error import line[{idx}]", exc_info=ex)

    async def __download_image(self, url: str) -> str | None:
        name_file = IMAGES_DIR / f'image_{uuid.uuid4()}.png'
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.is_success:
                async with aiofiles.open(name_file, mode="wb") as file:
                    await file.write(response.read())
            else:
                self.logger.error(f"No image loaded [{url}]")
        return name_file.__str__()
