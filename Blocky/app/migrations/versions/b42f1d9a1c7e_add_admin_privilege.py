"""Add administrator privilege to users.

Revision ID: b42f1d9a1c7e
Revises: a89cd7fdc083
"""
from alembic import op
import sqlalchemy as sa


revision = "b42f1d9a1c7e"
down_revision = "a89cd7fdc083"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.false()))
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.alter_column("is_admin", server_default=None)


def downgrade():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("is_admin")