"""add organizer study_count and records_count

Revision ID: c9d0e1f2a3b4
Revises: a7b8c9d0e1f2
Create Date: 2026-09-22 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c9d0e1f2a3b4"
down_revision: Union[str, Sequence[str], None] = "a7b8c9d0e1f2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "organizer",
        sa.Column(
            "study_count",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )
    op.add_column(
        "organizer",
        sa.Column(
            "records_count",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.execute(
        """
        UPDATE organizer AS o
        SET study_count = (
            SELECT COUNT(*)
            FROM studies AS s
            WHERE s.organizer_id = o.id
        )
        """
    )
    op.execute(
        """
        UPDATE organizer AS o
        SET records_count = (
            SELECT COUNT(*)
            FROM randomization_records AS r
            INNER JOIN studies AS s ON r.study_id = s.id
            WHERE s.organizer_id = o.id
        )
        """
    )


def downgrade() -> None:
    op.drop_column("organizer", "records_count")
    op.drop_column("organizer", "study_count")
