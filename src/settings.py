import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

# Path
BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / "media/images"

# Data Base
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

DATABASE_URL_SYNC = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
DATABASE_URL_ASYNC = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")
MENU_IMAGE_FILE_ID = os.getenv("MENU_IMAGE_FILE_ID")

# Authentication Backend Admin
SECRET_KEY = os.getenv("SECRET_KEY")

LOG_DIR = BASE_DIR / "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        },
        "db_handler": {
            "class": "src.db_logger.db_log_handler.DatabaseLogHandler",
            "level": "INFO",
        },
        "project_file": {
            "class": "logging.FileHandler",
            "filename": LOG_DIR / "general.log",
            "formatter": "default",
        },
    },
    "loggers": {
        "": {
            "handlers": ["stdout", "project_file"],
            "level": "INFO",
            "propagate": True
        },
        "db": {
            "handlers": ["db_handler"],
        }
    }
}
