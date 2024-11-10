"""Added column payload to job table

Revision ID: 9956913ab521
Revises: ce85b51580d3
Create Date: 2024-09-17 15:05:13.766861

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2
import sqlmodel  

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9956913ab521'
down_revision = 'ce85b51580d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job', sa.Column('payload', postgresql.JSONB(astext_type=sa.Text()), nullable=True), schema='customer')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('job', 'payload', schema='customer')
    # ### end Alembic commands ###