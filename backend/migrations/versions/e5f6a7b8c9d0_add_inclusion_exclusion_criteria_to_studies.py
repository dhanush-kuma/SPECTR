"""add_inclusion_exclusion_criteria_to_studies

Revision ID: e5f6a7b8c9d0
Revises: a1b2c3d4e5f6
Create Date: 2026-09-16 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e5f6a7b8c9d0"
down_revision: Union[str, Sequence[str], None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "studies",
        sa.Column("inclusion_exclusion_criteria", sa.JSON(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("studies", "inclusion_exclusion_criteria")
