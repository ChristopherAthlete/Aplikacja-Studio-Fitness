# Baza danych

## Schematy

| Schemat           | Przeznaczenie                          | Zarządzanie                          |
| ----------------- | -------------------------------------- | ------------------------------------ |
| `fitness`         | Dane aplikacji                         | Alembic                              |
| `fitness_test`    | Testy integracyjne                     | `database/002_fitness_test_schema.sql` |
| `test_connection` | Test połączenia                        | `database/001_test_connection.sql`   |

## Tabele

### `fitness.klienci`

| Kolumna        | Typ           | Uwagi                       |
| -------------- | ------------- | --------------------------- |
| `id`           | BIGINT        | Identity, PK                |
| `imie`         | VARCHAR(60)   | wymagane                    |
| `nazwisko`     | VARCHAR(80)   | wymagane                    |
| `email`        | VARCHAR(254)  | opcjonalne                  |
| `telefon`      | VARCHAR(30)   | opcjonalne, format E.164    |
| `utworzono_at` | TIMESTAMPTZ   | domyślnie `now()`           |

### `fitness.trenerzy`

| Kolumna         | Typ          | Uwagi              |
| --------------- | ------------ | ------------------ |
| `id`            | BIGINT       | Identity, PK       |
| `imie`          | VARCHAR(60)  | wymagane           |
| `nazwisko`      | VARCHAR(80)  | wymagane           |
| `specjalizacja` | VARCHAR(120) | opcjonalne         |
| `utworzono_at`  | TIMESTAMPTZ  | domyślnie `now()`  |

### `fitness.sale`

| Kolumna        | Typ         | Uwagi                   |
| -------------- | ----------- | ----------------------- |
| `id`           | BIGINT      | Identity, PK            |
| `nazwa`        | VARCHAR(80) | wymagane, `UNIQUE`      |
| `pojemnosc`    | INTEGER     | `CHECK (pojemnosc > 0)` |
| `utworzono_at` | TIMESTAMPTZ | domyślnie `now()`       |

### `fitness.oferta_zajec`

Katalog zajęć grupowych i treningów indywidualnych.

| Kolumna             | Typ                    | Uwagi                       |
| ------------------- | ---------------------- | --------------------------- |
| `id`                | BIGINT                 | Identity, PK                |
| `nazwa`             | VARCHAR(120)           | wymagane                    |
| `opis`              | VARCHAR(1000)          | opcjonalne                  |
| `typ`               | `fitness.typ_zajec`    | wymagane                    |
| `poziom`            | `fitness.poziom_zajec` | opcjonalne                  |
| `czas_trwania_min`  | INTEGER                | `CHECK (> 0)`               |
| `cena`              | NUMERIC(8, 2)          | `CHECK (>= 0)`              |
| `limit_uczestnikow` | INTEGER                | `CHECK (> 0)`               |
| `utworzono_at`      | TIMESTAMPTZ            | domyślnie `now()`           |

Dodatkowo `CHECK (typ <> 'indywidualne' OR limit_uczestnikow = 1)`.

### `fitness.oferta_karnetow`

| Kolumna        | Typ           | Uwagi                                    |
| -------------- | ------------- | ---------------------------------------- |
| `id`           | BIGINT        | Identity, PK                             |
| `nazwa`        | VARCHAR(120)  | wymagane                                 |
| `cena`         | NUMERIC(8, 2) | `CHECK (>= 0)`                           |
| `liczba_wejsc` | INTEGER       | `NULL` = karnet open, inaczej `> 0`      |
| `dni_waznosci` | INTEGER       | `CHECK (> 0)`                            |
| `utworzono_at` | TIMESTAMPTZ   | domyślnie `now()`                        |

## Typy wyliczeniowe

| Typ                    | Wartości                                   |
| ---------------------- | ------------------------------------------ |
| `fitness.typ_zajec`    | `grupowe`, `indywidualne`                  |
| `fitness.poziom_zajec` | `poczatkujacy`, `sredni`, `zaawansowany`   |

W Pythonie: `TypZajec`, `PoziomZajec` (`app/models.py`). Dodanie wartości
wymaga migracji (`ALTER TYPE ... ADD VALUE`) oraz zmiany w
`database/002_fitness_test_schema.sql`.

## Migracje (Alembic)

Komendy uruchamiane z folderu `backend`:

```bash
alembic upgrade head                              # zastosowanie migracji
alembic revision --autogenerate -m "opis zmiany"  # nowa migracja
```

- Autogenerate obsługuje tylko schemat `fitness` (filtr `include_name` w `migrations/env.py`).
- Nowy schemat trzeba utworzyć ręcznie w migracji: `op.execute("CREATE SCHEMA IF NOT EXISTS ...")`.
- Każdą wygenerowaną migrację należy przejrzeć przed commitem.

## TODO

- Diagram ERD
- Kolejne tabele
