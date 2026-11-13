from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import Mock

import pytest
from app.database import get_db
from app.main import app
from app.models import OfertaZajec, PoziomZajec, TypZajec
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError, OperationalError


@pytest.fixture
def fake_db():
    # Symulowana baza danych: przy add() nadajemy id i datę jak PostgreSQL
    db = Mock()

    def fake_add(obj):
        obj.id = 1
        obj.utworzono_at = datetime.now(UTC)

    db.add.side_effect = fake_add

    app.dependency_overrides[get_db] = lambda: db

    try:
        yield db
    finally:
        app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def client(fake_db):
    with TestClient(app) as test_client:
        yield test_client


GRUPOWE_ZAJECIA = {
    "nazwa": "Joga",
    "opis": "Zajęcia rozciągające",
    "typ": "grupowe",
    "poziom": "poczatkujacy",
    "czas_trwania_min": 60,
    "cena": "40.00",
    "limit_uczestnikow": 15,
}


# Trenerzy


def test_create_trainer(client, fake_db):
    response = client.post(
        "/api/trainers",
        json={"imie": "Jan", "nazwisko": "Kowalski", "specjalizacja": "Crossfit"},
    )

    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["specjalizacja"] == "Crossfit"
    fake_db.commit.assert_called_once()


def test_create_trainer_without_name(client, fake_db):
    response = client.post("/api/trainers", json={"nazwisko": "Kowalski"})

    assert response.status_code == 422
    fake_db.add.assert_not_called()


def test_get_trainer_not_found(client, fake_db):
    fake_db.get.return_value = None

    response = client.get("/api/trainers/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Nie znaleziono trenera"


def test_create_trainer_database_error(client, fake_db):
    fake_db.commit.side_effect = OperationalError("COMMIT", {}, Exception("down"))

    response = client.post(
        "/api/trainers", json={"imie": "Jan", "nazwisko": "Kowalski"}
    )

    assert response.status_code == 500
    fake_db.rollback.assert_called_once()


# Sale


def test_create_room(client, fake_db):
    response = client.post("/api/rooms", json={"nazwa": "Sala A", "pojemnosc": 20})

    assert response.status_code == 201
    assert response.json()["nazwa"] == "Sala A"
    fake_db.commit.assert_called_once()


def test_create_room_with_zero_capacity(client, fake_db):
    response = client.post("/api/rooms", json={"nazwa": "Sala A", "pojemnosc": 0})

    assert response.status_code == 422
    fake_db.add.assert_not_called()


def test_create_room_duplicate_name(client, fake_db):
    fake_db.commit.side_effect = IntegrityError("INSERT", {}, Exception("unique"))

    response = client.post("/api/rooms", json={"nazwa": "Sala A", "pojemnosc": 20})

    assert response.status_code == 409
    assert response.json()["detail"] == "Sala o takiej nazwie już istnieje"
    fake_db.rollback.assert_called_once()


# Oferta zajęć


def test_create_activity(client, fake_db):
    response = client.post("/api/activities", json=GRUPOWE_ZAJECIA)

    assert response.status_code == 201
    assert response.json()["typ"] == "grupowe"
    assert response.json()["poziom"] == "poczatkujacy"
    assert Decimal(response.json()["cena"]) == Decimal("40.00")
    fake_db.commit.assert_called_once()


def test_create_individual_activity_without_level(client, fake_db):
    response = client.post(
        "/api/activities",
        json={
            "nazwa": "Trening personalny",
            "typ": "indywidualne",
            "czas_trwania_min": 60,
            "cena": "150.00",
            "limit_uczestnikow": 1,
        },
    )

    assert response.status_code == 201
    assert response.json()["poziom"] is None


def test_create_individual_activity_with_many_participants(client, fake_db):
    response = client.post(
        "/api/activities",
        json={**GRUPOWE_ZAJECIA, "typ": "indywidualne", "limit_uczestnikow": 2},
    )

    assert response.status_code == 422
    fake_db.add.assert_not_called()


@pytest.mark.parametrize(
    "field, value",
    [
        ("typ", "online"),
        ("poziom", "ekspert"),
        ("czas_trwania_min", 0),
        ("cena", "-1.00"),
        ("cena", "10.999"),
        ("limit_uczestnikow", 0),
        ("nazwa", ""),
    ],
)
def test_create_activity_invalid_data(client, fake_db, field, value):
    response = client.post("/api/activities", json={**GRUPOWE_ZAJECIA, field: value})

    assert response.status_code == 422
    fake_db.add.assert_not_called()


def test_get_activities_with_filters(client, fake_db):
    zajecia = OfertaZajec(
        nazwa="Joga",
        typ=TypZajec.GRUPOWE,
        poziom=PoziomZajec.POCZATKUJACY,
        czas_trwania_min=60,
        cena=Decimal("40.00"),
        limit_uczestnikow=15,
    )
    zajecia.id = 1
    zajecia.utworzono_at = datetime.now(UTC)

    fake_db.scalars.return_value.all.return_value = [zajecia]

    response = client.get("/api/activities?typ=grupowe&poziom=poczatkujacy")

    assert response.status_code == 200
    assert response.json()[0]["nazwa"] == "Joga"

    # Zapytanie do bazy powinno zawierać oba filtry
    statement = str(fake_db.scalars.call_args.args[0])
    assert "oferta_zajec.typ =" in statement
    assert "oferta_zajec.poziom =" in statement


def test_get_activities_invalid_filter(client, fake_db):
    response = client.get("/api/activities?typ=online")

    assert response.status_code == 422
    fake_db.scalars.assert_not_called()


# Oferta karnetów


def test_create_open_pass_offer(client, fake_db):
    response = client.post(
        "/api/pass-offers",
        json={"nazwa": "Open miesięczny", "cena": "199.00", "dni_waznosci": 30},
    )

    assert response.status_code == 201
    assert response.json()["liczba_wejsc"] is None
    fake_db.commit.assert_called_once()


def test_create_pass_offer_with_entries(client, fake_db):
    response = client.post(
        "/api/pass-offers",
        json={
            "nazwa": "10 wejść",
            "cena": "250.00",
            "liczba_wejsc": 10,
            "dni_waznosci": 60,
        },
    )

    assert response.status_code == 201
    assert response.json()["liczba_wejsc"] == 10


@pytest.mark.parametrize(
    "field, value",
    [("liczba_wejsc", 0), ("dni_waznosci", 0), ("cena", "-5.00")],
)
def test_create_pass_offer_invalid_data(client, fake_db, field, value):
    data = {"nazwa": "10 wejść", "cena": "250.00", "dni_waznosci": 60}

    response = client.post("/api/pass-offers", json={**data, field: value})

    assert response.status_code == 422
    fake_db.add.assert_not_called()


def test_get_pass_offer_not_found(client, fake_db):
    fake_db.get.return_value = None

    response = client.get("/api/pass-offers/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Nie znaleziono karnetu w ofercie"
