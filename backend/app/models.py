import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    Enum,
    Identity,
    Integer,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TypZajec(enum.StrEnum):
    GRUPOWE = "grupowe"
    INDYWIDUALNE = "indywidualne"


class PoziomZajec(enum.StrEnum):
    POCZATKUJACY = "poczatkujacy"
    SREDNI = "sredni"
    ZAAWANSOWANY = "zaawansowany"


def _enum_values(enum_class: type[enum.Enum]) -> list[str]:
    # W bazie zapisujemy wartości ("grupowe"), a nie nazwy ("GRUPOWE")
    return [member.value for member in enum_class]


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


class Trener(Base):
    __tablename__ = "trenerzy"
    __table_args__ = {"schema": "fitness"}

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)

    imie: Mapped[str] = mapped_column(String(60))
    nazwisko: Mapped[str] = mapped_column(String(80))
    specjalizacja: Mapped[str | None] = mapped_column(String(120))

    utworzono_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Sala(Base):
    __tablename__ = "sale"
    __table_args__ = (
        CheckConstraint("pojemnosc > 0", name="ck_sale_pojemnosc"),
        {"schema": "fitness"},
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)

    nazwa: Mapped[str] = mapped_column(String(80), unique=True)
    pojemnosc: Mapped[int] = mapped_column(Integer)

    utworzono_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class OfertaZajec(Base):
    __tablename__ = "oferta_zajec"
    __table_args__ = (
        CheckConstraint("czas_trwania_min > 0", name="ck_oferta_zajec_czas"),
        CheckConstraint("cena >= 0", name="ck_oferta_zajec_cena"),
        CheckConstraint("limit_uczestnikow > 0", name="ck_oferta_zajec_limit"),
        # Trening indywidualny to zawsze jeden uczestnik
        CheckConstraint(
            "typ <> 'indywidualne' OR limit_uczestnikow = 1",
            name="ck_oferta_zajec_indywidualne_limit",
        ),
        {"schema": "fitness"},
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)

    nazwa: Mapped[str] = mapped_column(String(120))
    opis: Mapped[str | None] = mapped_column(String(1000))

    typ: Mapped[TypZajec] = mapped_column(
        Enum(
            TypZajec,
            name="typ_zajec",
            schema="fitness",
            values_callable=_enum_values,
        )
    )
    poziom: Mapped[PoziomZajec | None] = mapped_column(
        Enum(
            PoziomZajec,
            name="poziom_zajec",
            schema="fitness",
            values_callable=_enum_values,
        )
    )

    czas_trwania_min: Mapped[int] = mapped_column(Integer)
    cena: Mapped[Decimal] = mapped_column(Numeric(8, 2))
    limit_uczestnikow: Mapped[int] = mapped_column(Integer)

    utworzono_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class OfertaKarnetu(Base):
    __tablename__ = "oferta_karnetow"
    __table_args__ = (
        CheckConstraint("cena >= 0", name="ck_oferta_karnetow_cena"),
        CheckConstraint(
            "liczba_wejsc IS NULL OR liczba_wejsc > 0",
            name="ck_oferta_karnetow_wejscia",
        ),
        CheckConstraint("dni_waznosci > 0", name="ck_oferta_karnetow_dni"),
        {"schema": "fitness"},
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)

    nazwa: Mapped[str] = mapped_column(String(120))
    cena: Mapped[Decimal] = mapped_column(Numeric(8, 2))

    # NULL = karnet open (bez limitu wejść)
    liczba_wejsc: Mapped[int | None] = mapped_column(Integer)
    dni_waznosci: Mapped[int] = mapped_column(Integer)

    utworzono_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
