from datetime import UTC, datetime
from unittest.mock import Mock

from app.database import get_db
from app.main import app
from app.models import Klient
from fastapi.testclient import TestClient


def test_create_client():
    # Symulowana baza danych
    fake_db = Mock()

    def fake_add(klient):
        klient.id = 1
        klient.utworzono_at = datetime.now(UTC)

    fake_db.add.side_effect = fake_add

    # Zastępujemy prawdziwą sesję testową
    app.dependency_overrides[get_db] = lambda: fake_db

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/clients",
                json={
                    "imie": "Anna",
                    "nazwisko": "Nowak",
                    "email": "anna@example.com",
                    "telefon": None,
                },
            )
    finally:
        app.dependency_overrides.pop(get_db, None)

    # Sprawdzamy wynik
    assert response.status_code == 201
    assert response.json()["imie"] == "Anna"
    assert response.json()["nazwisko"] == "Nowak"

    # Sprawdzamy, czy backend próbował zapisać dane
    fake_db.add.assert_called_once()
    fake_db.commit.assert_called_once()


def test_create_client_without_lastname():
    fake_db = Mock()

    app.dependency_overrides[get_db] = lambda: fake_db

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/clients",
                json={"imie": "Anna", "email": "anna@example.com", "telefon": None},
            )
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert response.status_code == 422
    fake_db.add.assert_not_called()
    fake_db.commit.assert_not_called()


def test_get_clients():
    fake_db = Mock()

    klient = Klient(
        imie="Anna", nazwisko="Nowak", email="anna@example.com", telefon=None
    )

    klient.id = 1
    klient.utworzono_at = datetime.now(UTC)

    # Symulujemy wynik zapytania do bazy
    fake_db.scalars.return_value.all.return_value = [klient]

    app.dependency_overrides[get_db] = lambda: fake_db

    try:
        with TestClient(app) as client:
            response = client.get("/api/clients")
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["imie"] == "Anna"
    assert response.json()[0]["nazwisko"] == "Nowak"

    fake_db.scalars.assert_called_once()
    fake_db.commit.assert_not_called()
