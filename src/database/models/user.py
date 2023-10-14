from typing import TYPE_CHECKING, Optional, List
from datetime import datetime

from sqlalchemy import ForeignKey, Integer
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database import Base

if TYPE_CHECKING:
    from .program import Program
    from .history import HistoryExercise


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True)
    program_id: Mapped[Optional[int]] = mapped_column(ForeignKey("program.id"))

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.current_timestamp(),
        nullable=True,
    )

    program: Mapped[Optional["Program"]] = relationship(back_populates="users")
    history_exercises: Mapped[List["HistoryExercise"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"User [{self.id}]"
