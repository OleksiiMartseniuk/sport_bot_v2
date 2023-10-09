from typing import Optional, List
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Enum
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.utils.utils import Week


class TimestampBase(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        server_onupdate=func.current_timestamp(),
    )


class Category(TimestampBase):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), unique=True)

    programs: Mapped[List["Program"]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return self.title


class Program(TimestampBase):
    __tablename__ = "program"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))

    category: Mapped["Category"] = relationship(back_populates="programs")
    exercises: Mapped[list["Exercise"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return self.title


class Exercise(TimestampBase):
    __tablename__ = "exercise"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    number_of_approaches: Mapped[int] = mapped_column(Integer)
    number_of_repetitions: Mapped[int] = mapped_column(Integer)
    image: Mapped[str] = mapped_column(String)
    telegram_image_id: Mapped[str] = mapped_column(String(255))
    day: Mapped[Optional[Enum]] = mapped_column(
        Enum(Week),
        nullable=True,
    )
    program_id: Mapped[int] = mapped_column(ForeignKey("program.id"))

    program: Mapped["Program"] = relationship(back_populates="exercises")

    def __repr__(self):
        return self.title
