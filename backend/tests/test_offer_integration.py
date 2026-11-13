from decimal import Decimal
from uuid import uuid4


def test_create_and_read_trainer(test_api_client):
    response = test_api_client.post(
        "/api/trainers",
        json={"imie": "Test", "nazwisko": "Trener", "specjalizacja": "Joga"},
    )

    assert response.status_code == 201, response.text
    created = response.json()

    response = test_api_client.get(f"/api/trainers/{created['id']}")

    assert response.status_code == 200, response.text
    assert response.json() == created


def test_create_room_duplicate_name(test_api_client):
    nazwa = f"Sala {uuid4().hex[:8]}"

    response = test_api_client.post(
        "/api/rooms", json={"nazwa": nazwa, "pojemnosc": 20}
    )
    assert response.status_code == 201, response.text

    # Unikalność nazwy pilnuje baza (UNIQUE), nie walidacja Pydantic
    response = test_api_client.post(
        "/api/rooms", json={"nazwa": nazwa, "pojemnosc": 10}
    )
    assert response.status_code == 409, response.text

    # Po błędzie sesja nadal działa
    response = test_api_client.get("/api/rooms")
    assert response.status_code == 200, response.text
    assert sum(room["nazwa"] == nazwa for room in response.json()) == 1


def test_create_and_filter_activities(test_api_client):
    nazwa = f"Joga {uuid4().hex[:8]}"

    response = test_api_client.post(
        "/api/activities",
        json={
            "nazwa": nazwa,
            "typ": "grupowe",
            "poziom": "sredni",
            "czas_trwania_min": 60,
            "cena": "40",
            "limit_uczestnikow": 15,
        },
    )
    assert response.status_code == 201, response.text
    created = response.json()

    # Cena wraca z bazy jako NUMERIC(8, 2)
    assert Decimal(created["cena"]) == Decimal("40.00")

    response = test_api_client.get("/api/activities?typ=grupowe&poziom=sredni")
    assert response.status_code == 200, response.text
    assert any(activity["id"] == created["id"] for activity in response.json())

    response = test_api_client.get("/api/activities?typ=indywidualne")
    assert response.status_code == 200, response.text
    assert all(activity["id"] != created["id"] for activity in response.json())


def test_create_and_read_open_pass_offer(test_api_client):
    response = test_api_client.post(
        "/api/pass-offers",
        json={"nazwa": "Open miesięczny", "cena": "199.00", "dni_waznosci": 30},
    )
    assert response.status_code == 201, response.text
    created = response.json()

    response = test_api_client.get(f"/api/pass-offers/{created['id']}")

    assert response.status_code == 200, response.text
    assert response.json()["liczba_wejsc"] is None
    assert Decimal(response.json()["cena"]) == Decimal("199.00")
