import os
from collections.abc import Generator
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session

# Ściezka do env w folderze backend
env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(env_path)

# Konfiguracja połączenia PostgreSQL
database_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    host=os.environ["DB_HOST"],
    port=int(os.environ["DB_PORT"]),
    database=os.environ["DB_NAME"],
    query={"sslmode": "require"},
)

# Silnik połączenia z bazą
engine = create_engine(
    database_url,
    pool_pre_ping=True,
)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
