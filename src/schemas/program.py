from pydantic import BaseModel


class Category(BaseModel):
    title: str


class Program(BaseModel):
    title: str
    category_id: int


class Exercise(BaseModel):
    title: str
    number_of_approaches: int
    number_of_repetitions: int
    image: str
    telegram_image_id: str | None
    day: str
    program_id: int
