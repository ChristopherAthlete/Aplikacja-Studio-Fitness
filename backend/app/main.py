import logging
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .database import engine, get_db
from .models import Klient
from .schemas import KlientCreate, KlientResponse

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
