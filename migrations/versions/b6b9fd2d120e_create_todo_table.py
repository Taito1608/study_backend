"""create_todo_table

Revision ID: b6b9fd2d120e
Revises: f1df1ba86def
Create Date: 2025-01-28 14:45:29.655085

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6b9fd2d120e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('todo',
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("box", sa.String(length=200), nullable=False),
    sa.Column("date", sa.String(length=100),nullable=False),
    sa.Column("done", sa.Boolean, default=False),
    sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f('ix_todo_id'), 'todo', ['id'], unique=False)
    


def downgrade() -> None:
    op.drop_index(op.f('ix_todo_id'), table_name='todo')
    op.drop_table('todo')
