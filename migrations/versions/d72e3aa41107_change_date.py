from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = 'd72e3aa41107'
down_revision = '2f438095d52a'
branch_labels = None
depends_on = None

def upgrade():
    # 新しいテーブルを作成
    op.create_table(
        'todo_new',
        sa.Column('todo_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('box', sa.String(200), nullable=False),
        sa.Column('date', sa.Date, nullable=True),  # Date型に変更
        sa.Column('completed', sa.Boolean, default=False),
    )

    # 古いデータをコピー
    op.execute('INSERT INTO todo_new (todo_id, box, date, completed) SELECT todo_id, box, date, completed FROM todo')

    # 古いテーブルを削除
    op.drop_table('todo')

    # 新しいテーブルの名前を元に戻す
    op.rename_table('todo_new', 'todo')

def downgrade():
    # 元の DateTime に戻す場合の手順
    op.create_table(
        'todo_old',
        sa.Column('todo_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('box', sa.String(200), nullable=False),
        sa.Column('date', sa.DateTime, nullable=True),  # もとの DateTime に戻す
        sa.Column('completed', sa.Boolean, default=False),
    )

    op.execute('INSERT INTO todo_old (todo_id, box, date, completed) SELECT todo_id, box, date, completed FROM todo')

    op.drop_table('todo')

    op.rename_table('todo_old', 'todo')
