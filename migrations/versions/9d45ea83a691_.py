"""empty message

Revision ID: 9d45ea83a691
Revises: 7f55f0718e09
Create Date: 2019-06-27 22:14:39.079086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d45ea83a691'
down_revision = '7f55f0718e09'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('logindate', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'logindate')
    # ### end Alembic commands ###
