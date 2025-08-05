"""add user_id to transcript

Revision ID: 0e81bfc0e92a
Revises: 
Create Date: 2025-08-05 14:36:13.905137

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e81bfc0e92a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Tambah kolom user_id nullable=True
    with op.batch_alter_table('transcript', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
    # Isi semua baris dengan user_id default (misal 1)
    op.execute('UPDATE transcript SET user_id=1')
    # Alter kolom user_id jadi nullable=False dan tambah foreign key
    with op.batch_alter_table('transcript', schema=None) as batch_op:
        batch_op.alter_column('user_id', nullable=False)
        batch_op.create_foreign_key('fk_transcript_user_id', 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    with op.batch_alter_table('transcript', schema=None) as batch_op:
        batch_op.drop_constraint('fk_transcript_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
