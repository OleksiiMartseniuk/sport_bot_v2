from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Enum
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database import Base
from src.utils.utils import Week

if TYPE_CHECKING:
    from .user import User
    from .history import HistoryExercise


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), unique=True)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.current_timestamp(),
        nullable=True,
    )

    programs: Mapped[List["Program"]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return self.title


class Program(Base):
    __tablename__ = "program"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.current_timestamp(),
        nullable=True,
    )

    category: Mapped["Category"] = relationship(back_populates="programs")
    users: Mapped[List["User"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan",
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
        return self.title


class Exercise(Base):
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

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.current_timestamp(),
        nullable=True,
    )

    program: Mapped["Program"] = relationship(back_populates="exercises")
    history_exercises: Mapped[List["HistoryExercise"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return self.title
