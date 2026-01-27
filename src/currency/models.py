import datetime

from sqlalchemy import text
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from src.database import Base


class Ticker(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(nullable=False, index=True)
    price: Mapped[float] = mapped_column(nullable=False)
    timestamp: Mapped[int] = mapped_column(nullable=False, index=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text(
            "TIMEZONE('utc', now())")
    )