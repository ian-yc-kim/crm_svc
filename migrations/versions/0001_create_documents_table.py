from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001_create_documents_table'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # create documents table with types compatible for postgres and sqlite
    op.create_table(
        'documents',
        sa.Column('id', sa.String(length=36), primary_key=True, nullable=False),
        sa.Column('customer_id', sa.String(length=36), sa.ForeignKey('customers.id'), nullable=False),
        sa.Column('uploaded_by_user_id', sa.String(length=36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('original_filename', sa.String(), nullable=False),
        sa.Column('stored_filename', sa.String(), nullable=False, unique=True),
        sa.Column('file_path', sa.String(), nullable=False),
        sa.Column('file_type', sa.String(), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('virus_scan_status', sa.String(), nullable=False),
        sa.Column('access_level', sa.String(), nullable=False),
        sa.Column('metadata_json', postgresql.JSONB().with_variant(sa.JSON(), 'sqlite'), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('documents')
