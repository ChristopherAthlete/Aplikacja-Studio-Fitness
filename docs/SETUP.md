# Studio Fitness - uruchomienie lokalne

## Wymagania

- Python 3.12+
- Node.js LTS i npm
- Dostęp do testowej bazy PostgreSQL w Supabase
- Git

## 1. Pobranie projektu

Sklonuj repozytorium GitHub i otwórz folder projektu
w Visual Studio Code.

## 2. Backend FastAPI

Przejdź do folderu backend:

```bash
cd backend
```

Utwórz środowisko wirtualne:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Zainstaluj zależności:

```bash
python -m pip install -r requirements.txt
```

Utwórz plik `.env` na podstawie `.env.example`
i uzupełnij dane połączenia z Supabase.

Uruchom backend:

```bash
python -m uvicorn app.main:app --reload --port 8000
```

Dokumentacja API:

http://localhost:8000/docs

## 3. Baza danych

W Supabase SQL Editor wykonaj skrypt:

`database/001_test_connection.sql`

Skrypt tworzy tabelę wykorzystywaną
do testowania połączenia.

## 4. Frontend Next.js

Otwórz drugi terminal i przejdź do folderu frontend:

```bash
cd frontend
```

Zainstaluj zależności:

```bash
npm ci
```

Utwórz `.env.local` na podstawie `.env.example`.

Uruchom frontend:

```bash
npm run dev
```

Aplikacja:

http://localhost:3000

## 5. Weryfikacja działania

1. Otwórz `/test-connection`.
2. Kliknij „Sprawdź połączenie”.
3. Zapisz testową wiadomość.
4. Pobierz zapisane wiadomości.
5. Odśwież stronę i sprawdź ponownie odczyt.

Pomyślny zapis i odczyt potwierdzają działanie
Next.js → FastAPI → PostgreSQL.

## Uwagi

Projekt znajduje się w fazie rozwoju.

Testowe endpointy nie są zabezpieczone logowaniem
i nie powinny być udostępniane publicznie.

Nie dodawaj haseł, tokenów ani plików `.env`
do repozytorium.