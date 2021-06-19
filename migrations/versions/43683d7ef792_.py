"""empty message

Revision ID: 43683d7ef792
Revises: 07f692505120
Create Date: 2021-06-18 13:02:38.424161

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '43683d7ef792'
down_revision = '07f692505120'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('results')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('results',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('result_all', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('result_no_stop_words', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='results_pkey')
    )
    # ### end Alembic commands ###
