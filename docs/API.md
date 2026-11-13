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

## Oferta

Wspólne zasady:

- `POST` zwraca `201` i utworzony obiekt (z `id` i `utworzono_at`).
- `GET /{id}` zwraca `404`, gdy obiekt nie istnieje.
- Błędy: `422` (walidacja), `500` (błąd zapisu).
- Ceny to liczby z dwoma miejscami po przecinku (`NUMERIC(8, 2)`); w JSON
  zwracane jako tekst, np. `"40.00"`.

### Trenerzy

| Metoda | Ścieżka              | Opis              |
| ------ | -------------------- | ----------------- |
| GET    | `/api/trainers`      | Lista trenerów    |
| GET    | `/api/trainers/{id}` | Jeden trener      |
| POST   | `/api/trainers`      | Dodanie trenera   |

```json
{ "imie": "Jan", "nazwisko": "Kowalski", "specjalizacja": "Crossfit" }
```

- `specjalizacja`: opcjonalna, do 120 znaków

### Sale

| Metoda | Ścieżka           | Opis           |
| ------ | ----------------- | -------------- |
| GET    | `/api/rooms`      | Lista sal      |
| GET    | `/api/rooms/{id}` | Jedna sala     |
| POST   | `/api/rooms`      | Dodanie sali   |

```json
{ "nazwa": "Sala A", "pojemnosc": 20 }
```

- `nazwa`: unikalna, duplikat zwraca `409`
- `pojemnosc`: > 0

### Oferta zajęć

| Metoda | Ścieżka                | Opis                                   |
| ------ | ---------------------- | -------------------------------------- |
| GET    | `/api/activities`      | Lista, filtry `?typ=` i `?poziom=`     |
| GET    | `/api/activities/{id}` | Jedna pozycja                          |
| POST   | `/api/activities`      | Dodanie zajęć do oferty                |

```json
{
  "nazwa": "Joga",
  "opis": "Zajęcia rozciągające",
  "typ": "grupowe",
  "poziom": "poczatkujacy",
  "czas_trwania_min": 60,
  "cena": "40.00",
  "limit_uczestnikow": 15
}
```

- `typ`: `grupowe` | `indywidualne`
- `poziom`: `poczatkujacy` | `sredni` | `zaawansowany` | `null`
- `czas_trwania_min`, `limit_uczestnikow`: > 0; dla `indywidualne` limit musi być `1`
- `cena`: >= 0
- `opis`: opcjonalny, do 1000 znaków

### Oferta karnetów

| Metoda | Ścieżka                 | Opis                      |
| ------ | ----------------------- | ------------------------- |
| GET    | `/api/pass-offers`      | Lista karnetów w ofercie  |
| GET    | `/api/pass-offers/{id}` | Jeden karnet              |
| POST   | `/api/pass-offers`      | Dodanie karnetu do oferty |

```json
{ "nazwa": "10 wejść", "cena": "250.00", "liczba_wejsc": 10, "dni_waznosci": 60 }
```

- `liczba_wejsc`: > 0 albo `null` (karnet open, bez limitu wejść)
- `dni_waznosci`: > 0
- `cena`: >= 0

## TODO

- Edycja i usuwanie klientów oraz pozycji oferty
- Paginacja / wyszukiwanie po stronie API
- Autoryzacja
