from typing import TYPE_CHECKING, Optional, List

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database import Base
from src.database.mixins import TimestampMixin

if TYPE_CHECKING:
    from .program import Program
    from .history import HistoryExercise


class User(TimestampMixin, Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True)
    program_id: Mapped[Optional[int]] = mapped_column(ForeignKey("program.id"))

    program: Mapped[Optional["Program"]] = relationship(back_populates="users")
    history_exercises: Mapped[List["HistoryExercise"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"User [{self.id}]"
