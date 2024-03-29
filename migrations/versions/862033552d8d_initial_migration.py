"""Initial migration

Revision ID: 862033552d8d
Revises: ae2b408177d3
Create Date: 2023-11-15 08:05:19.044186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '862033552d8d'
down_revision = 'ae2b408177d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blood_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('blood_group', sa.String(length=5), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('request_date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blood_request')
    # ### end Alembic commands ###
