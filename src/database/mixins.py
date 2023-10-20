from typing import Optional
from datetime import datetime

from sqlalchemy import text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        onupdate=datetime.utcnow,
        nullable=True,
    )
