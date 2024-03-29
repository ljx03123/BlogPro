"""empty message

Revision ID: 60f85d7dee4f
Revises: 4d7aa021a6ef
Create Date: 2019-06-22 17:13:56.382239

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '60f85d7dee4f'
down_revision = '4d7aa021a6ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('category', 'fatherid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category', sa.Column('fatherid', mysql.VARCHAR(length=50), nullable=True))
    # ### end Alembic commands ###
