from uuid import uuid4


def test_create_and_read_client(test_api_client):
    email = f"test-{uuid4().hex}@example.com"

    # 1. Dodanie klienta
    response = test_api_client.post(
        "/api/clients",
        json={
            "imie": "Test",
            "nazwisko": "Integracyjny",
            "email": email,
            "telefon": None,
        },
    )

    assert response.status_code == 201, response.text

    created = response.json()
    assert created["imie"] == "Test"
    assert created["id"] > 0

    # 2. Pobranie klientów
    response = test_api_client.get("/api/clients")

    assert response.status_code == 200, response.text

    clients = response.json()

    # 3. Sprawdzenie zapisanego klienta
    assert any(
        client["id"] == created["id"] and client["email"] == email for client in clients
    )
