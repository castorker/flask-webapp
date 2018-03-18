"""tags

Revision ID: 8dbf7b985f9c
Revises: 640bbf9fe3c3
Create Date: 2018-03-18 17:55:25.118898

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8dbf7b985f9c'
down_revision = '640bbf9fe3c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=25), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tag_name'), 'tag', ['name'], unique=True)
    op.create_table('quibble_tag',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('quibble_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['quibble_id'], ['quibble.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('quibble_tag')
    op.drop_index(op.f('ix_tag_name'), table_name='tag')
    op.drop_table('tag')
    # ### end Alembic commands ###