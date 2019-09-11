"""add port to IPcamera table

Revision ID: 7341b42e6f62
Revises: c74114dde04d
Create Date: 2019-08-14 11:31:52.753858

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7341b42e6f62'
down_revision = 'c74114dde04d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ip_camera', sa.Column('port', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ip_camera', 'port')
    # ### end Alembic commands ###