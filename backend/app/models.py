from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Identity, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Klient(Base):
    __tablename__ = "klienci"
    __table_args__ = {"schema": "fitness"}

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)

    imie: Mapped[str] = mapped_column(String(60))
    nazwisko: Mapped[str] = mapped_column(String(80))

    email: Mapped[str | None] = mapped_column(String(254))
    telefon: Mapped[str | None] = mapped_column(String(30))

    utworzono_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
