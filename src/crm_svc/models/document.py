import uuid
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

from .base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    # Defer foreign key creation to avoid metadata resolution errors in tests
    customer_id = Column(
        String(36),
        ForeignKey('customers.id', name='fk_documents_customer_id', use_alter=True),
        nullable=False,
    )
    uploaded_by_user_id = Column(
        String(36),
        ForeignKey('users.id', name='fk_documents_uploaded_by_user_id', use_alter=True),
        nullable=False,
    )
    original_filename = Column(String, nullable=False)
    stored_filename = Column(String, unique=True, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    virus_scan_status = Column(String, nullable=False)
    access_level = Column(String, nullable=False)
    # Use JSONB for Postgres and JSON for Sqlite
    metadata_json = Column(JSONB().with_variant(sa.JSON(), "sqlite"), nullable=True)

    def __repr__(self) -> str:
        return f"<Document(id={self.id}, original_filename='{self.original_filename}')>"
