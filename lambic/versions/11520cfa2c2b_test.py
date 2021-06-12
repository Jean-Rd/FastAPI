"""TEST

Revision ID: 11520cfa2c2b
Revises: 9f27c2c29f7b
Create Date: 2021-06-10 23:09:56.477051

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11520cfa2c2b'
down_revision = '9f27c2c29f7b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Blogs', sa.Column('ad', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Blogs', 'ad')
    # ### end Alembic commands ###