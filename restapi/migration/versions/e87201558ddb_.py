"""empty message

Revision ID: e87201558ddb
Revises: 8f5c2da6e1d4
Create Date: 2023-12-26 20:37:27.867572

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e87201558ddb'
down_revision: Union[str, None] = '8f5c2da6e1d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('instrument',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('asset', sa.Column('instrument_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'asset', 'instrument', ['instrument_id'], ['id'])
    op.drop_column('asset', 'instrument_type_id')
    op.add_column('asset_ratio', sa.Column('instrument', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'asset_ratio', 'instrument', ['instrument'], ['id'])
    op.drop_column('asset_ratio', 'instrument_type_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('asset_ratio', sa.Column('instrument_type_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'asset_ratio', type_='foreignkey')
    op.create_foreign_key('asset_ratio_instrument_type_id_fkey', 'asset_ratio', 'instrument_types', ['instrument_type_id'], ['id'])
    op.drop_column('asset_ratio', 'instrument')
    op.add_column('asset', sa.Column('instrument_type_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'asset', type_='foreignkey')
    op.create_foreign_key('asset_instrument_type_id_fkey', 'asset', 'instrument_types', ['instrument_type_id'], ['id'])
    op.drop_column('asset', 'instrument_id')
    op.create_table('instrument_types',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('type_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='instrument_types_pkey')
    )
    op.drop_table('instrument')
    # ### end Alembic commands ###
