from pydantic import BaseModel

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
