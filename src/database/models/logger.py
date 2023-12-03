from typing import Optional
from datetime import datetime

from sqlalchemy import text
from sqlalchemy import String, Enum, Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.database import Base
from src.utils.utils import LogLevel


class StatusLog(Base):
    __tablename__ = "status_log"

    id: Mapped[int] = mapped_column(primary_key=True)
    logger_name: Mapped[str] = mapped_column(String(255))
    level: Mapped[Enum] = mapped_column(Enum(LogLevel))
    msg: Mapped[str] = mapped_column(String)
    trace: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
    )

    def __repr__(self):
        return f"Log: {self.level} - {self.msg}"
