# Architektura

## Stos technologiczny

| Warstwa  | Technologie                                          |
| -------- | ---------------------------------------------------- |
| Frontend | Next.js 16, React 19, Tailwind 4, shadcn/ui, Phosphor |
| Backend  | FastAPI, SQLAlchemy 2, Pydantic 2, Alembic           |
| Baza     | PostgreSQL (Supabase)                                |

## Przepływ danych

```
Next.js (localhost:3000) → fetch → FastAPI (localhost:8000) → SQLAlchemy → PostgreSQL
```

Adres API frontend bierze z `NEXT_PUBLIC_API_URL`.
CORS w backendzie dopuszcza tylko `localhost:3000`, metody GET i POST.

## Struktura katalogów

```
backend/
  app/          # main.py (endpointy), models.py, schemas.py, database.py
  migrations/   # Alembic
  tests/
database/       # ręczne skrypty SQL
frontend/src/
  app/          # trasy (App Router)
  components/   # komponenty domenowe (np. clients/)
  components/ui # komponenty shadcn
  hooks/, lib/
```

## Trasy frontendu

| Trasa              | Opis                          |
| ------------------ | ----------------------------- |
| `/`                | Panel główny                  |
| `/clients`         | Lista i dodawanie klientów    |
| `/dashboard`       | TODO                          |
| `/test-connection` | Test połączenia z bazą        |

## TODO

- Uwierzytelnianie
- Kolejne moduły (rezerwacje, treningi, członkostwa)
- Wdrożenie
