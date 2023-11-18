from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database import Base
from src.database.mixins import TimestampMixin

if TYPE_CHECKING:
    from .program import Exercise, Program
    from .user import User


class HistoryExercise(TimestampMixin, Base):
    __tablename__ = "history_exercise"

    id: Mapped[int] = mapped_column(primary_key=True)
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercise.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    program_id: Mapped[int] = mapped_column(ForeignKey("program.id"))

    approach: Mapped[int] = mapped_column(Integer)
    number_of_repetitions: Mapped[int] = mapped_column(Integer)

    exercise: Mapped["Exercise"] = relationship(
        back_populates="history_exercises",
    )
    program: Mapped["Program"] = relationship(
        back_populates="history_exercises",
    )
    user: Mapped["User"] = relationship(
        back_populates="history_exercises",
    )

    def __repr__(self):
        return (
            f"HistoryExercise [{self.id}] exercise_id={self.exercise_id} "
            f"user_id={self.user_id}, program_id={self.program_id}"
        )
