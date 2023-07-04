"""add content column

Revision ID: 9a52fe7e0cc2
Revises: cb711dc40fb6
Create Date: 2023-07-04 10:19:47.243255

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a52fe7e0cc2'
down_revision = 'cb711dc40fb6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass