from typing import TYPE_CHECKING, Optional, List

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from src.database import Base
from src.database.mixins import TimestampMixin

if TYPE_CHECKING:
    from .program import Program
    from .history import HistoryExercise
    from .token import Token


class TelegramUser(TimestampMixin, Base):
    __tablename__ = "telegram_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[Optional[str]]
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True)
    program_id: Mapped[Optional[int]] = mapped_column(ForeignKey("program.id"))
    is_schedule: Mapped[bool] = mapped_column(
        server_default=expression.false(),
    )

    program: Mapped[Optional["Program"]] = relationship(
        back_populates="telegram_users",
    )
    history_exercises: Mapped[List["HistoryExercise"]] = relationship(
        back_populates="telegram_user",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"[{self.id}] TelegramUser - {self.username}"


class User(TimestampMixin, Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    token: Mapped["Token"] = relationship(back_populates="user")

    def __repr__(self):
        return f"[{self.id} User - {self.username}]"
