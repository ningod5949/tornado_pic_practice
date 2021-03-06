"""add thumb url for posts

Revision ID: 2ccd17d1e470
Revises: 9b65b921e66b
Create Date: 2019-05-24 16:20:22.935039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ccd17d1e470'
down_revision = '9b65b921e66b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('thumb_url', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'thumb_url')
    # ### end Alembic commands ###
