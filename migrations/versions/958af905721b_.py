"""empty message

Revision ID: 958af905721b
Revises: a219c7fbb507
Create Date: 2021-06-22 16:12:56.442247

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '958af905721b'
down_revision = 'a219c7fbb507'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'seeking_description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_description', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
