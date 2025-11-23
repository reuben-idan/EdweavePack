"""Add institution and role fields to users

Revision ID: 002
Revises: 001
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    # Add institution and role columns to users table
    op.add_column('users', sa.Column('institution', sa.String(), nullable=True))
    op.add_column('users', sa.Column('role', sa.String(), nullable=False, server_default='teacher'))

def downgrade():
    # Remove institution and role columns from users table
    op.drop_column('users', 'role')
    op.drop_column('users', 'institution')