# Testy

## Uruchomienie

Z folderu `backend`:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```

## Rodzaje testów

### Jednostkowe

Np. `tests/test_clients.py`. Sesja bazy jest podmieniana na `Mock`:

```python
app.dependency_overrides[get_db] = lambda: fake_db
```

Nie wymagają połączenia z bazą.

### Integracyjne

Np. `tests/test_clients_integration.py`, z fixture'em `test_api_client` z `conftest.py`:

- `schema_translate_map` przekierowuje `fitness` na `fitness_test`,
- każdy test działa w transakcji wycofywanej na końcu,
- wymagają istniejących tabel w schemacie `fitness_test` (fixture sprawdza
  wszystkie tabele z `Base.metadata` i zgłasza brakującą).

### Przygotowanie schematu `fitness_test`

Uruchom `database/002_fitness_test_schema.sql` w Supabase (SQL Editor).
Skrypt jest idempotentny, więc po dodaniu nowych tabel wystarczy go
uruchomić ponownie.

Przy każdej nowej tabeli lub zmianie struktury w `fitness` trzeba
zaktualizować ten skrypt, żeby `fitness_test` odpowiadał migracjom.

## TODO

- Testy frontendu
- Uruchamianie testów w CI
