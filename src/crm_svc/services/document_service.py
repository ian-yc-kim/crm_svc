import logging
from typing import List, Tuple, Optional
from uuid import UUID

from fastapi import HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from crm_svc.schemas.document import DocumentResponse, VirusScanStatus
from crm_svc.utils.file_storage import (
    _validate_file_size,
    _get_file_type,
    _save_file_to_disk,
    _get_file_content,
    _delete_file_from_disk,
)

logger = logging.getLogger(__name__)


class DocumentService:
    """Service handling document operations."""

    @staticmethod
    def perform_virus_scan(file_content: bytes) -> VirusScanStatus:
        # Placeholder: integrate real virus scanner here in future
        return VirusScanStatus.CLEAN

    def upload_document(
        self,
        db: Session,
        customer_id: UUID,
        uploaded_by_user_id: UUID,
        file: UploadFile,
        access_level: str,
        metadata: Optional[dict] = None,
    ) -> DocumentResponse:
        try:
            file_content = file.file.read()
        except Exception as e:
            logger.error(e, exc_info=True)
            raise HTTPException(status_code=400, detail="Failed to read uploaded file")

        try:
            _validate_file_size(file_content)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        try:
            file_type = _get_file_type(file_content, file.filename)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        scan_status = self.perform_virus_scan(file_content)
        if scan_status == VirusScanStatus.INFECTED:
            raise HTTPException(status_code=400, detail="File infected by virus")

        try:
            stored_filename, file_path = _save_file_to_disk(file_content, file.filename, customer_id)
        except IOError as e:
            logger.error(e, exc_info=True)
            raise HTTPException(status_code=500, detail="Failed to save file")

        # Delay importing model to avoid circular imports
        try:
            from crm_svc.models import Document

            doc = Document(
                customer_id=str(customer_id),
                uploaded_by_user_id=str(uploaded_by_user_id),
                original_filename=file.filename,
                stored_filename=stored_filename,
                file_path=file_path,
                file_type=file_type,
                file_size=len(file_content),
                virus_scan_status=scan_status.value,
                access_level=access_level,
                metadata_json=metadata,
            )
            db.add(doc)
            db.commit()
            db.refresh(doc)
            return DocumentResponse.model_validate(doc)
        except Exception as e:
            logger.error(e, exc_info=True)
            # attempt cleanup
            try:
                _delete_file_from_disk(file_path)
            except Exception:
                logger.error("Failed to cleanup saved file after DB error", exc_info=True)
            raise HTTPException(status_code=500, detail="Failed to persist document metadata")

    def get_document_metadata(self, db: Session, document_id: UUID) -> DocumentResponse:
        from crm_svc.models import Document

        try:
            stmt = select(Document).where(Document.id == str(document_id))
            result = db.execute(stmt).scalars().one_or_none()
            if result is None:
                raise HTTPException(status_code=404, detail="Document not found")
            return DocumentResponse.model_validate(result)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(e, exc_info=True)
            raise HTTPException(status_code=500, detail="Failed to fetch document metadata")

    def list_documents_for_customer(self, db: Session, customer_id: UUID) -> List[DocumentResponse]:
        from crm_svc.models import Document

        try:
            stmt = select(Document).where(Document.customer_id == str(customer_id))
            results = db.execute(stmt).scalars().all()
            return [DocumentResponse.model_validate(r) for r in results]
        except Exception as e:
            logger.error(e, exc_info=True)
            raise HTTPException(status_code=500, detail="Failed to list documents")

    def download_document(self, db: Session, document_id: UUID) -> Tuple[bytes, str, str]:
        from crm_svc.models import Document

        try:
            stmt = select(Document).where(Document.id == str(document_id))
            result = db.execute(stmt).scalars().one_or_none()
            if result is None:
                raise HTTPException(status_code=404, detail="Document not found")
            content = _get_file_content(result.file_path)
            return content, result.original_filename, result.file_type
        except HTTPException:
            raise
        except IOError as e:
            logger.error(e, exc_info=True)
            raise HTTPException(status_code=500, detail="Failed to read stored file")
        except Exception as e:
            logger.error(e, exc_info=True)
            raise HTTPException(status_code=500, detail="Failed to download document")

    def delete_document(self, db: Session, document_id: UUID) -> None:
        from crm_svc.models import Document

        try:
            stmt = select(Document).where(Document.id == str(document_id))
            result = db.execute(stmt).scalars().one_or_none()
            if result is None:
                raise HTTPException(status_code=404, detail="Document not found")
            try:
                _delete_file_from_disk(result.file_path)
            except IOError as e:
                logger.error(e, exc_info=True)
                raise HTTPException(status_code=500, detail="Failed to delete stored file")
            try:
                db.delete(result)
                db.commit()
            except Exception as e:
                logger.error(e, exc_info=True)
                raise HTTPException(status_code=500, detail="Failed to delete document record")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(e, exc_info=True)
            raise HTTPException(status_code=500, detail="Failed to delete document")
