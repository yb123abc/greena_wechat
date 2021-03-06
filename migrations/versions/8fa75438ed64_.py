"""empty message

Revision ID: 8fa75438ed64
Revises: 56ea7744bfc0
Create Date: 2016-05-17 21:57:43.093908

"""

# revision identifiers, used by Alembic.
revision = '8fa75438ed64'
down_revision = '56ea7744bfc0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('provinces',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('citys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('province_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['province_id'], ['provinces.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('districts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['city_id'], ['citys.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('districts')
    op.drop_table('citys')
    op.drop_table('provinces')
    ### end Alembic commands ###
