from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database import Base
from src.database.mixins import TimestampMixin

if TYPE_CHECKING:
    from .user import User


class Token(TimestampMixin, Base):
    __tablename__ = "token"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String(50), unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(
        back_populates="token",
        single_parent=True
    )

    def __repr__(self):
        return f"[{self.id}] Token user - {self.user_id}"
