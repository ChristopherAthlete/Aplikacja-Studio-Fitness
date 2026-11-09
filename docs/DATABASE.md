# Baza danych

## Schematy

| Schemat           | Przeznaczenie                          | Zarządzanie                          |
| ----------------- | -------------------------------------- | ------------------------------------ |
| `fitness`         | Dane aplikacji                         | Alembic                              |
| `fitness_test`    | Testy integracyjne                     | TODO: opisać, jak tworzyć            |
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
