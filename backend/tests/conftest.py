import pytest
from app.database import engine, get_db
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.orm import Session


@pytest.fixture
def test_api_client():
    with engine.connect().execution_options(
        schema_translate_map={"fitness": "fitness_test"}
    ) as connection:
        transaction = connection.begin()

        try:
            # Sprawdzenie istnienia tabeli testowej
            table_exists = connection.execute(
                text("SELECT to_regclass('fitness_test.klienci')")
            ).scalar_one()

            if table_exists is None:
                raise RuntimeError("Brak tabeli fitness_test.klienci")

            def override_get_db():
                with Session(
                    bind=connection, join_transaction_mode="create_savepoint"
                ) as session:
                    yield session

            app.dependency_overrides[get_db] = override_get_db

            with TestClient(app) as client:
                yield client

        finally:
            app.dependency_overrides.pop(get_db, None)
            transaction.rollback()
