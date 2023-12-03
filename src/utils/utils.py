import enum
import uuid
import logging

import httpx
import aiofiles

from src.settings import IMAGES_DIR


logger = logging.getLogger("db")


class Week(enum.Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class LogLevel(enum.Enum):
    CRITICAL = logging.CRITICAL
    FATAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    WARN = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET


WeekDict = {
    0: "Понедельник",
    1: "Вторник",
    2: "Середа",
    3: "Четверг",
    4: "Пятница",
    5: "Суббота",
    6: "Воскресение",
}


async def download_image(url: str) -> str | None:
    name_file = IMAGES_DIR / f'image_{uuid.uuid4()}.png'
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
        except Exception as ex:
            logger.error(f"Error download image {url=}", exc_info=ex)
            return None
        if response.is_success:
            async with aiofiles.open(name_file, mode="wb") as file:
                await file.write(response.read())
                return name_file.__str__()
        else:
            logger.error(f"No image loaded {response.status_code=} [{url=}]")
            return None
