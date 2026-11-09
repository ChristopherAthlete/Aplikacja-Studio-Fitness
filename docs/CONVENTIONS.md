# Konwencje

## Język

- Nazwy domenowe po polsku: `Klient`, `klienci`, `imie`, `utworzono_at`.
- Nazwy techniczne i URL-e po angielsku: `/api/clients`, `create_client`, `ClientsPage`.
- Komentarze i komunikaty w UI oraz błędach API po polsku.

## Backend

- Schematy Pydantic: `XCreate` (wejście) oraz `XResponse(XCreate)` z `from_attributes=True`.
- Sesja bazy wstrzykiwana przez `DbSession = Annotated[Session, Depends(get_db)]`.
- Przy błędzie zapisu: `db.rollback()`, `logger.exception(...)`, `HTTPException` z polskim komunikatem.
- Modele tabel w schemacie `fitness` (`__table_args__ = {"schema": "fitness"}`).

## Frontend

- Komponenty domenowe w `components/<moduł>/`, w `components/ui/` tylko komponenty shadcn.
- Importy przez alias `@/`.
- Ikony: Phosphor (`@phosphor-icons/react`).
- Pobieranie danych w `useEffect` z `AbortController`.
- Telefon normalizowany do E.164 przez `libphonenumber-js` przed wysłaniem do API.

## Git

- Commity w stylu Conventional Commits: `feat:`, `fix:`, `test:`, `chore:`, `docs:`.
- Branche `feature/<moduł>`, merge do `main` przez Pull Request.

## TODO

- Formatowanie / linting backendu (np. ruff)
- Zasady code review
