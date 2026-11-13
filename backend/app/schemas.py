from datetime import datetime
from decimal import Decimal
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .models import PoziomZajec, TypZajec


class KlientCreate(BaseModel):
    imie: str = Field(min_length=1, max_length=60)
    nazwisko: str = Field(min_length=1, max_length=80)
    email: str | None = None
    telefon: str | None = None


class KlientResponse(KlientCreate):
    id: int
    utworzono_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TrenerCreate(BaseModel):
    imie: str = Field(min_length=1, max_length=60)
    nazwisko: str = Field(min_length=1, max_length=80)
    specjalizacja: str | None = Field(default=None, max_length=120)


class TrenerResponse(TrenerCreate):
    id: int
    utworzono_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SalaCreate(BaseModel):
    nazwa: str = Field(min_length=1, max_length=80)
    pojemnosc: int = Field(gt=0)


class SalaResponse(SalaCreate):
    id: int
    utworzono_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OfertaZajecCreate(BaseModel):
    nazwa: str = Field(min_length=1, max_length=120)
    opis: str | None = Field(default=None, max_length=1000)
    typ: TypZajec
    poziom: PoziomZajec | None = None
    czas_trwania_min: int = Field(gt=0)
    cena: Decimal = Field(ge=0, max_digits=8, decimal_places=2)
    limit_uczestnikow: int = Field(gt=0)

    @model_validator(mode="after")
    def check_limit_indywidualne(self) -> Self:
        if self.typ == TypZajec.INDYWIDUALNE and self.limit_uczestnikow != 1:
            raise ValueError("Trening indywidualny musi mieć limit 1 uczestnika")
        return self


class OfertaZajecResponse(OfertaZajecCreate):
    id: int
    utworzono_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OfertaKarnetuCreate(BaseModel):
    nazwa: str = Field(min_length=1, max_length=120)
    cena: Decimal = Field(ge=0, max_digits=8, decimal_places=2)
    liczba_wejsc: int | None = Field(default=None, gt=0)
    dni_waznosci: int = Field(gt=0)


class OfertaKarnetuResponse(OfertaKarnetuCreate):
    id: int
    utworzono_at: datetime

    model_config = ConfigDict(from_attributes=True)
