from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import ForeignKey, Integer
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database import Base

if TYPE_CHECKING:
    from .program import Program


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True)
    program_id: Mapped[int] = mapped_column(ForeignKey("program.id"))

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.current_timestamp(),
        nullable=True,
    )

    program: Mapped["Program"] = relationship(back_populates="users")

    def __repr__(self):
        return f"User [{self.id}]"
