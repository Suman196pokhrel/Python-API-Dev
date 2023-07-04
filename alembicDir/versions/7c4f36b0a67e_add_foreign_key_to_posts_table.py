"""add foreign key to posts table

Revision ID: 7c4f36b0a67e
Revises: edd8e5c72f58
Create Date: 2023-07-04 11:14:24.437045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c4f36b0a67e'
down_revision = 'edd8e5c72f58'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk',source_table='posts',referent_table='users',local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts','user_id')
    pass
