from enum import Enum

from aiogram.filters.callback_data import CallbackData


class MenuLevels(str, Enum):
    category = "category"
    program = "program"
    day = "day"
    exercises = "exercises"
    exercise = "exercise"


class ProgramCallback(CallbackData, prefix="program"):
    menu_level: MenuLevels
    category: int
    program: int
    day: int
    exercise: int
