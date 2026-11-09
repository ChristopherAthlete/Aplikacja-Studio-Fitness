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
- wymagają istniejącej tabeli `fitness_test.klienci`.

## TODO

- Jak przygotować schemat `fitness_test`
- Testy frontendu
- Uruchamianie testów w CI
