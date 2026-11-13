import logging
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from .database import engine, get_db
from .models import (
    Base,
    Klient,
    OfertaKarnetu,
    OfertaZajec,
    PoziomZajec,
    Sala,
    Trener,
    TypZajec,
)
from .schemas import (
    KlientCreate,
    KlientResponse,
    OfertaKarnetuCreate,
    OfertaKarnetuResponse,
    OfertaZajecCreate,
    OfertaZajecResponse,
    SalaCreate,
    SalaResponse,
    TrenerCreate,
    TrenerResponse,
)

logger = logging.getLogger(__name__)

# Inicjalizacja aplikacji
app = FastAPI(title="Studio Fitness B API", version="0.1.0")

DbSession = Annotated[Session, Depends(get_db)]

# Połączenie z frontendem Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


def save_or_500[T: Base](db: Session, obj: T, error_message: str) -> T:
    """Zapisuje obiekt; przy błędzie bazy robi rollback i zwraca 500."""
    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)

    except SQLAlchemyError:
        db.rollback()
        logger.exception(error_message)
        raise HTTPException(status_code=500, detail=error_message)

    return obj


def get_or_404[T: Base](
    db: Session, model: type[T], obj_id: int, not_found: str
) -> T:
    obj = db.get(model, obj_id)

    if obj is None:
        raise HTTPException(status_code=404, detail=not_found)

    return obj


# Model danych testowej wiadomości
class TestMessage(BaseModel):
    message: str = Field(min_length=1, max_length=200)


# 1. Sprawdzenie działania backendu
@app.get("/api/health")
def health():
    return {"status": "ok", "service": "studio-fitness-b"}


# 2. Sprawdzenie połączenia z Supabase
@app.get("/api/db-check")
def check_database():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {"status": "ok", "database": "connected"}

    except SQLAlchemyError:
        logger.exception("Błąd połączenia z PostgreSQL")
        raise HTTPException(
            status_code=503, detail="Nie udało się połączyć z bazą danych"
        )


# 3. Zapis wiadomości do Supabase
@app.post("/api/test-messages", status_code=201)
def create_test_message(data: TestMessage):
    message = data.message.strip()

    if not message:
        raise HTTPException(status_code=422, detail="Wiadomość nie może być pusta")

    with engine.begin() as connection:
        result = connection.execute(
            text("""
                INSERT INTO test_connection.messages (message)
                VALUES (:message)
                RETURNING id, message
            """),
            {"message": message},
        )

        return dict(result.mappings().one())


# 4. Odczyt wiadomości z Supabase
@app.get("/api/test-messages")
def get_test_messages():
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT id, message
                FROM test_connection.messages
                ORDER BY id DESC
                LIMIT 20
            """)
        )

        return [dict(row) for row in result.mappings()]


@app.post("/api/clients", response_model=KlientResponse, status_code=201)
def create_client(data: KlientCreate, db: DbSession):
    klient = Klient(**data.model_dump())

    try:
        db.add(klient)
        db.commit()
        db.refresh(klient)

    except SQLAlchemyError:
        db.rollback()
        logger.exception("Bład podczas dodawania klienta")
        raise HTTPException(status_code=500, detail="Nie udało się dodać klienta")

    return klient


@app.get("/api/clients", response_model=list[KlientResponse])
def get_clients(db: DbSession):
    statement = select(Klient).order_by(Klient.id)

    clients = db.scalars(statement).all()

    return clients


# Trenerzy


@app.post("/api/trainers", response_model=TrenerResponse, status_code=201)
def create_trainer(data: TrenerCreate, db: DbSession):
    return save_or_500(
        db, Trener(**data.model_dump()), "Nie udało się dodać trenera"
    )


@app.get("/api/trainers", response_model=list[TrenerResponse])
def get_trainers(db: DbSession):
    return db.scalars(select(Trener).order_by(Trener.id)).all()


@app.get("/api/trainers/{trainer_id}", response_model=TrenerResponse)
def get_trainer(trainer_id: int, db: DbSession):
    return get_or_404(db, Trener, trainer_id, "Nie znaleziono trenera")


# Sale


@app.post("/api/rooms", response_model=SalaResponse, status_code=201)
def create_room(data: SalaCreate, db: DbSession):
    sala = Sala(**data.model_dump())

    try:
        db.add(sala)
        db.commit()
        db.refresh(sala)

    except IntegrityError:
        # Jedyne ograniczenie, którego nie łapie walidacja Pydantic: unikalna nazwa
        db.rollback()
        raise HTTPException(
            status_code=409, detail="Sala o takiej nazwie już istnieje"
        )

    except SQLAlchemyError:
        db.rollback()
        logger.exception("Błąd podczas dodawania sali")
        raise HTTPException(status_code=500, detail="Nie udało się dodać sali")

    return sala


@app.get("/api/rooms", response_model=list[SalaResponse])
def get_rooms(db: DbSession):
    return db.scalars(select(Sala).order_by(Sala.id)).all()


@app.get("/api/rooms/{room_id}", response_model=SalaResponse)
def get_room(room_id: int, db: DbSession):
    return get_or_404(db, Sala, room_id, "Nie znaleziono sali")


# Oferta zajęć


@app.post("/api/activities", response_model=OfertaZajecResponse, status_code=201)
def create_activity(data: OfertaZajecCreate, db: DbSession):
    return save_or_500(
        db, OfertaZajec(**data.model_dump()), "Nie udało się dodać zajęć do oferty"
    )


@app.get("/api/activities", response_model=list[OfertaZajecResponse])
def get_activities(
    db: DbSession,
    typ: TypZajec | None = None,
    poziom: PoziomZajec | None = None,
):
    statement = select(OfertaZajec).order_by(OfertaZajec.id)

    if typ is not None:
        statement = statement.where(OfertaZajec.typ == typ)

    if poziom is not None:
        statement = statement.where(OfertaZajec.poziom == poziom)

    return db.scalars(statement).all()


@app.get("/api/activities/{activity_id}", response_model=OfertaZajecResponse)
def get_activity(activity_id: int, db: DbSession):
    return get_or_404(db, OfertaZajec, activity_id, "Nie znaleziono zajęć w ofercie")


# Oferta karnetów


@app.post("/api/pass-offers", response_model=OfertaKarnetuResponse, status_code=201)
def create_pass_offer(data: OfertaKarnetuCreate, db: DbSession):
    return save_or_500(
        db,
        OfertaKarnetu(**data.model_dump()),
        "Nie udało się dodać karnetu do oferty",
    )


@app.get("/api/pass-offers", response_model=list[OfertaKarnetuResponse])
def get_pass_offers(db: DbSession):
    return db.scalars(select(OfertaKarnetu).order_by(OfertaKarnetu.id)).all()


@app.get("/api/pass-offers/{offer_id}", response_model=OfertaKarnetuResponse)
def get_pass_offer(offer_id: int, db: DbSession):
    return get_or_404(
        db, OfertaKarnetu, offer_id, "Nie znaleziono karnetu w ofercie"
    )
