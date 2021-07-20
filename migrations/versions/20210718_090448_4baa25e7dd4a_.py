"""empty message

Revision ID: 4baa25e7dd4a
Revises: 68f2a7e4c892
Create Date: 2021-07-18 09:04:48.589096

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session

# revision identifiers, used by Alembic.

revision = '4baa25e7dd4a'
down_revision = '68f2a7e4c892'
branch_labels = None
depends_on = None

session = Session(bind=op.get_bind())
session.execute('PRAGMA foreign_keys = OFF;')
session.commit()


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bac_points', schema=None) as batch_op:
        batch_op.drop_column('source')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bac_points', schema=None) as batch_op:
        batch_op.add_column(sa.Column('source', sa.Enum('OWN', 'MAPPING', name='sources'), server_default="OWN"))

    # ### end Alembic commands ###