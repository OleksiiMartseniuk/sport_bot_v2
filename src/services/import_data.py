import csv
import logging

from pydantic import BaseModel

from src.utils.utils import download_image
from src.utils.unitofwork import SqlAlchemyUnitOfWork
from src.utils.utils import Week


class File(BaseModel):
    category: str
    program: str
    exercise_title: str
    exercise_number_of_approaches: int
    exercise_number_of_repetitions: int
    exercise_rest: int
    exercise_image_url: str
    exercise_day: int

    def get_fields_exercise(self):
        exercise = {}
        for key, value in self.model_dump().items():
            if "exercise_image_url" in key:
                continue
            elif "exercise_day" in key:
                exercise["day"] = Week(value)
            elif "exercise_" in key:
                exercise[key.replace("exercise_", "")] = value
        return exercise


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
                    _, category = await self.uow.category.get_or_create(
                        title=obj.category
                    )
                    _, program = await self.uow.program.get_or_create(
                        title=obj.program,
                        category_id=category.id,
                    )
                    _, exercise = await self.uow.exercise.get_or_create(
                        program_id=program.id,
                        **obj.get_fields_exercise(),
                    )
                    if exercise.image is None:
                        image_path = await download_image(
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
