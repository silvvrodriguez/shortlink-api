"""create links table

Revision ID: 7df68c8ed018
Revises:
Create Date: 2026-09-14 19:52:04.094760
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7df68c8ed018"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the links table."""

    op.create_table(
        "links",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("original_url", sa.String(), nullable=False),
        sa.Column("short_code", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_links_short_code"),
        "links",
        ["short_code"],
        unique=True,
    )


def downgrade() -> None:
    """Remove the links table."""

    op.drop_index(
        op.f("ix_links_short_code"),
        table_name="links",
    )

    op.drop_table("links")