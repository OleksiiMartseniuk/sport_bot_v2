from typing import Optional

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.database import Base
from src.settings import IMAGE_MENU_PATH


class ProjectSettings(Base):
    __tablename__ = "project_settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    menu_image_path: Mapped[str] = mapped_column(
        default=IMAGE_MENU_PATH.as_posix(),
    )
    menu_image_telegram_id: Mapped[Optional[str]] = mapped_column()

    def __repr__(self):
        return "ProjectSettings"
