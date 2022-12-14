"""Adding User

Revision ID: 470f7011cafe
Revises: 
Create Date: 2022-08-31 11:24:44.806498

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '470f7011cafe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('User',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('telephone', sa.String(), nullable=True),
    sa.Column('hash_pw', sa.String(), nullable=False),
    sa.Column('avatar', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('token', sa.String(), nullable=True),
    sa.Column('token_created_at', sa.String(), nullable=True),
    sa.Column('work_for', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('User')
    # ### end Alembic commands ###
