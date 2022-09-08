"""Add notification table

Revision ID: e7bf6ac170dd
Revises: 4dbf8c3dfdef
Create Date: 2022-09-08 16:40:39.038930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7bf6ac170dd'
down_revision = '4dbf8c3dfdef'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Notification',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('sourcing_id', sa.Integer(), nullable=True),
    sa.Column('sourcing_type', sa.String(), nullable=True),
    sa.Column('sourcing_name', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('from_hospital_id', sa.Integer(), nullable=True),
    sa.Column('to_hospital_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_notification_sourcing_', 'Notification', ['sourcing_type', 'sourcing_id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_notification_sourcing_', table_name='Notification')
    op.drop_table('Notification')
    # ### end Alembic commands ###
