"""empty message

Revision ID: e1ef93f40d3d
Revises: de8a3de227ef
Create Date: 2018-12-03 12:35:01.505576

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'e1ef93f40d3d'
down_revision = 'de8a3de227ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task_status', sa.Column('is_artist_allowed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task_status', 'is_artist_allowed')
    # ### end Alembic commands ###
