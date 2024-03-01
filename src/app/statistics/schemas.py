from datetime import datetime

from pydantic import BaseModel

from src.utils.utils import Week


class CategorySchema(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime | None


class ProgramSchema(BaseModel):
    id: int
    title: str
    category: CategorySchema
    created_at: datetime
    updated_at: datetime | None


class ExercisesSchema(BaseModel):
    id: int
    title: str
    number_of_approaches: int
    number_of_repetitions: int
    rest: int | None
    image: str | None
    day: Week | None
    created_at: datetime
    updated_at: datetime | None


class HistoryExercisesSchema(BaseModel):
    id: int
    approach: int
    number_of_repetitions: int
    exercise: ExercisesSchema
    program: ProgramSchema
    created_at: datetime
    updated_at: datetime | None
