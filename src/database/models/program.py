from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.database.mixins import TimestampMixin
from src.utils.utils import Week

if TYPE_CHECKING:
    from .history import HistoryExercise
    from .user import TelegramUser


class Category(TimestampMixin, Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), unique=True)

    programs: Mapped[List["Program"]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"[{self.id}] {self.title}"


class Program(TimestampMixin, Base):
    __tablename__ = "program"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))

    category: Mapped["Category"] = relationship(
        back_populates="programs",
    )
    telegram_users: Mapped[List["TelegramUser"]] = relationship(
        back_populates="program",
    )
    exercises: Mapped[List["Exercise"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan",
    )
    history_exercises: Mapped[List["HistoryExercise"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"[{self.id}] {self.title}"


class Exercise(TimestampMixin, Base):
    __tablename__ = "exercise"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    number_of_approaches: Mapped[int] = mapped_column(Integer)
    number_of_repetitions: Mapped[int] = mapped_column(Integer)
    rest: Mapped[Optional[int]] = mapped_column(Integer)
    image: Mapped[Optional[str]] = mapped_column(String)
    telegram_image_id: Mapped[Optional[str]] = mapped_column(String(255))
    day: Mapped[Optional[Enum]] = mapped_column(
        Enum(Week),
        nullable=True,
    )
    program_id: Mapped[int] = mapped_column(ForeignKey("program.id"))

    program: Mapped["Program"] = relationship(
        back_populates="exercises",
    )
    history_exercises: Mapped[List["HistoryExercise"]] = relationship(
        back_populates="exercise",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"[{self.id}] {self.title}"
