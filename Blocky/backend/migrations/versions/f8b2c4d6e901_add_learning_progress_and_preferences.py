"""add learning progress and preferences

Revision ID: f8b2c4d6e901
Revises: e7f1a3c9b482
Create Date: 2026-09-07

"""
from alembic import op
import sqlalchemy as sa


revision = "f8b2c4d6e901"
down_revision = "e7f1a3c9b482"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("points", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("users", sa.Column("theme", sa.String(length=30), nullable=False, server_default="paper"))
    op.add_column("users", sa.Column("profile_picture", sa.LargeBinary(), nullable=True))
    op.add_column("users", sa.Column("profile_picture_type", sa.String(length=50), nullable=True))
    op.create_table(
        "lesson_progress",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("lesson_id", sa.String(length=80), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "lesson_id", name="uq_lesson_progress_user_lesson"),
    )
    op.create_index(op.f("ix_lesson_progress_user_id"), "lesson_progress", ["user_id"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_lesson_progress_user_id"), table_name="lesson_progress")
    op.drop_table("lesson_progress")
    op.drop_column("users", "profile_picture_type")
    op.drop_column("users", "profile_picture")
    op.drop_column("users", "theme")
    op.drop_column("users", "points")