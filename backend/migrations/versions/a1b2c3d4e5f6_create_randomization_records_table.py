"""create_randomization_records_table

Revision ID: a1b2c3d4e5f6
Revises: b2c3d4e5f6a7
Create Date: 2026-09-06 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "b2c3d4e5f6a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "randomization_records",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "study_id",
            sa.Integer(),
            sa.ForeignKey("studies.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("sequence_number", sa.Integer(), nullable=False),
        sa.Column("kit_code", sa.String(length=100), nullable=False),
        sa.Column("treatment_name", sa.String(length=255), nullable=False),
        sa.Column("assigned_patient_id", sa.String(length=255), nullable=True),
        sa.Column(
            "assigned_by_investigator_id",
            sa.Integer(),
            sa.ForeignKey("investigator.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("assigned_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "blind",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
        sa.Column(
            "site_id",
            sa.Integer(),
            sa.ForeignKey("sites.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "strata_id",
            sa.Integer(),
            sa.ForeignKey("stratas.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.UniqueConstraint(
            "study_id",
            "sequence_number",
            name="uq_randomization_records_study_sequence",
        ),
    )
    op.create_index(
        "uq_randomization_records_study_patient",
        "randomization_records",
        ["study_id", sa.text("lower(assigned_patient_id)")],
        unique=True,
        postgresql_where=sa.text("assigned_patient_id IS NOT NULL"),
    )


def downgrade() -> None:
    op.drop_index(
        "uq_randomization_records_study_patient",
        table_name="randomization_records",
    )
    op.drop_table("randomization_records")
