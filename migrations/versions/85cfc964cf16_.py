"""empty message

Revision ID: 85cfc964cf16
Revises: 
Create Date: 2019-06-21 22:30:03.729379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85cfc964cf16'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('asname', sa.String(length=100), nullable=True),
    sa.Column('keyword', sa.String(length=100), nullable=True),
    sa.Column('descript', sa.Text(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('asname'),
    sa.UniqueConstraint('name')
    )
    op.create_table('article',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('text', sa.Text(length=5000), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('categoryid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['categoryid'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('article')
    op.drop_table('category')
    # ### end Alembic commands ###
