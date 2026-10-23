from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class KlientCreate(BaseModel):
    imie: str = Field(min_length=1, max_length=60)
    nazwisko: str = Field(min_length=1, max_length=80)
    email: str | None = None
    telefon: str | None = None


class KlientResponse(KlientCreate):
    id: int
    utworzono_at: datetime

    model_config = ConfigDict(from_attributes=True)
