"""create offer tables

Revision ID: a3f1c9e27b54
Revises: ce927828dcf6
Create Date: 2026-11-13 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "a3f1c9e27b54"
down_revision: str | Sequence[str] | None = "ce927828dcf6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


# create_type=False: typy tworzymy i usuwamy jawnie poniżej
typ_zajec = postgresql.ENUM(
    "grupowe", "indywidualne", name="typ_zajec", schema="fitness", create_type=False
)
poziom_zajec = postgresql.ENUM(
    "poczatkujacy",
    "sredni",
    "zaawansowany",
    name="poziom_zajec",
    schema="fitness",
    create_type=False,
)


def upgrade() -> None:
    """Upgrade schema."""
    typ_zajec.create(op.get_bind(), checkfirst=True)
    poziom_zajec.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "trenerzy",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("imie", sa.String(length=60), nullable=False),
        sa.Column("nazwisko", sa.String(length=80), nullable=False),
        sa.Column("specjalizacja", sa.String(length=120), nullable=True),
        sa.Column(
            "utworzono_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="fitness",
    )

    op.create_table(
        "sale",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("nazwa", sa.String(length=80), nullable=False),
        sa.Column("pojemnosc", sa.Integer(), nullable=False),
        sa.Column(
            "utworzono_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint("pojemnosc > 0", name="ck_sale_pojemnosc"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nazwa"),
        schema="fitness",
    )

    op.create_table(
        "oferta_zajec",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("nazwa", sa.String(length=120), nullable=False),
        sa.Column("opis", sa.String(length=1000), nullable=True),
        sa.Column("typ", typ_zajec, nullable=False),
        sa.Column("poziom", poziom_zajec, nullable=True),
        sa.Column("czas_trwania_min", sa.Integer(), nullable=False),
        sa.Column("cena", sa.Numeric(precision=8, scale=2), nullable=False),
        sa.Column("limit_uczestnikow", sa.Integer(), nullable=False),
        sa.Column(
            "utworzono_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint("czas_trwania_min > 0", name="ck_oferta_zajec_czas"),
        sa.CheckConstraint("cena >= 0", name="ck_oferta_zajec_cena"),
        sa.CheckConstraint("limit_uczestnikow > 0", name="ck_oferta_zajec_limit"),
        sa.CheckConstraint(
            "typ <> 'indywidualne' OR limit_uczestnikow = 1",
            name="ck_oferta_zajec_indywidualne_limit",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="fitness",
    )

    op.create_table(
        "oferta_karnetow",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("nazwa", sa.String(length=120), nullable=False),
        sa.Column("cena", sa.Numeric(precision=8, scale=2), nullable=False),
        sa.Column("liczba_wejsc", sa.Integer(), nullable=True),
        sa.Column("dni_waznosci", sa.Integer(), nullable=False),
        sa.Column(
            "utworzono_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint("cena >= 0", name="ck_oferta_karnetow_cena"),
        sa.CheckConstraint(
            "liczba_wejsc IS NULL OR liczba_wejsc > 0",
            name="ck_oferta_karnetow_wejscia",
        ),
        sa.CheckConstraint("dni_waznosci > 0", name="ck_oferta_karnetow_dni"),
        sa.PrimaryKeyConstraint("id"),
        schema="fitness",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("oferta_karnetow", schema="fitness")
    op.drop_table("oferta_zajec", schema="fitness")
    op.drop_table("sale", schema="fitness")
    op.drop_table("trenerzy", schema="fitness")

    poziom_zajec.drop(op.get_bind(), checkfirst=True)
    typ_zajec.drop(op.get_bind(), checkfirst=True)
