"""empty message

Revision ID: ef2c2260d73c
Revises: 958af905721b
Create Date: 2021-06-23 19:48:33.091082

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef2c2260d73c'
down_revision = '958af905721b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'phone')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('phone', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    # ### end Alembic commands ###