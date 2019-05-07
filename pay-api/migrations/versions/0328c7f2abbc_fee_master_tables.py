"""fee_master_tables

Revision ID: 0328c7f2abbc
Revises: 
Create Date: 2019-05-07 11:20:06.793469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0328c7f2abbc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('corp_type',
    sa.Column('corp_type_code', sa.String(length=10), nullable=False),
    sa.Column('corp_type_description', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('corp_type_code')
    )
    op.create_table('fee_code',
    sa.Column('fee_code', sa.String(length=10), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('fee_code')
    )
    op.create_table('filing_type',
    sa.Column('filing_type_code', sa.String(length=10), nullable=False),
    sa.Column('filing_description', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('filing_type_code')
    )
    op.create_table('fee_schedule',
    sa.Column('fee_schedule_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('filing_type_code', sa.String(length=10), nullable=False),
    sa.Column('corp_type_code', sa.String(length=10), nullable=False),
    sa.Column('fee_code', sa.String(length=10), nullable=False),
    sa.Column('fee_start_date', sa.Date(), nullable=False),
    sa.Column('fee_end_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['corp_type_code'], ['corp_type.corp_type_code'], ),
    sa.ForeignKeyConstraint(['fee_code'], ['fee_code.fee_code'], ),
    sa.ForeignKeyConstraint(['filing_type_code'], ['filing_type.filing_type_code'], ),
    sa.PrimaryKeyConstraint('fee_schedule_id'),
    sa.UniqueConstraint('filing_type_code', 'corp_type_code', 'fee_code', name='unique_fee_sched_1')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fee_schedule')
    op.drop_table('filing_type')
    op.drop_table('fee_code')
    op.drop_table('corp_type')
    # ### end Alembic commands ###
