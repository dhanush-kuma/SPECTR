"""create append-only audit_logs table

Revision ID: e1f2a3b4c5d6
Revises: d0e1f2a3b4c5
Create Date: 2026-09-24 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e1f2a3b4c5d6"
down_revision: Union[str, Sequence[str], None] = "d0e1f2a3b4c5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("randomization_record_id", sa.Integer(), nullable=False),
        sa.Column("study_id", sa.Integer(), nullable=False),
        sa.Column("study_title", sa.String(length=255), nullable=False),
        sa.Column("protocol_code", sa.String(length=100), nullable=False),
        sa.Column("study_status", sa.String(length=50), nullable=False),
        sa.Column("ctc_id", sa.Integer(), nullable=False),
        sa.Column("ctc_username", sa.String(length=255), nullable=False),
        sa.Column("site_investigator_id", sa.Integer(), nullable=False),
        sa.Column("site_investigator_username", sa.String(length=8), nullable=False),
        sa.Column("site_investigator_email", sa.String(length=255), nullable=False),
        sa.Column("site_investigator_name", sa.String(length=255), nullable=True),
        sa.Column("site_id", sa.Integer(), nullable=False),
        sa.Column("site_name", sa.String(length=255), nullable=False),
        sa.Column("strata_id", sa.Integer(), nullable=False),
        sa.Column("stratum_name", sa.String(length=255), nullable=False),
        sa.Column("participant_id", sa.String(length=255), nullable=False),
        sa.Column("sequence_number", sa.Integer(), nullable=False),
        sa.Column("kit_code", sa.String(length=100), nullable=False),
        sa.Column("treatment_arm", sa.String(length=255), nullable=False),
        sa.Column("blinding_type", sa.SmallInteger(), nullable=False),
        sa.Column("client_ip", sa.String(length=45), nullable=True),
        sa.Column("assigned_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    op.create_index(
        "ix_audit_logs_study_id_created_at",
        "audit_logs",
        ["study_id", "created_at"],
    )
    op.create_index(
        "ix_audit_logs_participant_id_study_id",
        "audit_logs",
        ["study_id", "participant_id"],
    )

    op.execute(
        """
        CREATE OR REPLACE FUNCTION audit_logs_deny_mutation()
        RETURNS trigger
        LANGUAGE plpgsql
        AS $$
        BEGIN
            RAISE EXCEPTION 'audit_logs is append-only: % is not allowed', TG_OP;
        END;
        $$;
        """
    )
    op.execute(
        """
        CREATE TRIGGER audit_logs_no_update
        BEFORE UPDATE ON audit_logs
        FOR EACH ROW
        EXECUTE PROCEDURE audit_logs_deny_mutation();
        """
    )
    op.execute(
        """
        CREATE TRIGGER audit_logs_no_delete
        BEFORE DELETE ON audit_logs
        FOR EACH ROW
        EXECUTE PROCEDURE audit_logs_deny_mutation();
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS audit_logs_no_delete ON audit_logs;")
    op.execute("DROP TRIGGER IF EXISTS audit_logs_no_update ON audit_logs;")
    op.execute("DROP FUNCTION IF EXISTS audit_logs_deny_mutation();")
    op.drop_index("ix_audit_logs_participant_id_study_id", table_name="audit_logs")
    op.drop_index("ix_audit_logs_study_id_created_at", table_name="audit_logs")
    op.drop_table("audit_logs")
