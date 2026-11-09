# API

Pełna, generowana dokumentacja: http://localhost:8000/docs

## Diagnostyka

| Metoda | Ścieżka          | Opis                                       |
| ------ | ---------------- | ------------------------------------------ |
| GET    | `/api/health`    | Status backendu                            |
| GET    | `/api/db-check`  | Test połączenia z bazą (503 przy błędzie)  |
| GET    | `/api/test-messages` | Ostatnie 20 wiadomości testowych       |
| POST   | `/api/test-messages` | Zapis wiadomości testowej              |

Endpointy testowe nie są zabezpieczone, do usunięcia przed wdrożeniem.

## Klienci

| Metoda | Ścieżka        | Opis                 |
| ------ | -------------- | -------------------- |
| GET    | `/api/clients` | Lista klientów       |
| POST   | `/api/clients` | Dodanie klienta (201)|

Przykładowe żądanie `POST /api/clients`:

```json
{
  "imie": "Anna",
  "nazwisko": "Nowak",
  "email": "anna@example.com",
  "telefon": "+48500100200"
}
```

- `imie`: wymagane, 1–60 znaków
- `nazwisko`: wymagane, 1–80 znaków
- `email`, `telefon`: opcjonalne

Odpowiedź zawiera dodatkowo `id` i `utworzono_at`.

Błędy: `422` (walidacja), `500` (błąd zapisu).

## TODO

- Edycja i usuwanie klientów
- Paginacja / wyszukiwanie po stronie API
- Autoryzacja
