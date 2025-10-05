import os
import tempfile
import uuid
import logging
import mimetypes
from typing import Tuple
from uuid import UUID

import filetype

from crm_svc.config import DOCUMENT_STORAGE_PATH, MAX_FILE_SIZE_MB

logger = logging.getLogger(__name__)

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # docx
    "image/jpeg",
    "image/png",
}


def _ensure_customer_dir(customer_id: UUID) -> str:
    path = os.path.join(DOCUMENT_STORAGE_PATH, str(customer_id))
    os.makedirs(path, exist_ok=True)
    return path


def _get_extension_from_filename(filename: str) -> str:
    _, ext = os.path.splitext(filename)
    return ext or ""


def _save_file_to_disk(file_content: bytes, original_filename: str, customer_id: UUID) -> Tuple[str, str]:
    """Save file bytes to disk under DOCUMENT_STORAGE_PATH/customer_id.

    Returns stored_filename and absolute file_path.
    """
    try:
        customer_dir = _ensure_customer_dir(customer_id)
        ext = _get_extension_from_filename(original_filename)
        stored_filename = f"{uuid.uuid4().hex}{ext}"
        tmp_fd, tmp_path = tempfile.mkstemp(dir=customer_dir)
        os.close(tmp_fd)
        try:
            with open(tmp_path, "wb") as f:
                f.write(file_content)
            final_path = os.path.join(customer_dir, stored_filename)
            os.replace(tmp_path, final_path)
            return stored_filename, os.path.abspath(final_path)
        finally:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
    except Exception as e:
        logger.error(e, exc_info=True)
        raise IOError("Failed to save file to disk") from e


def _delete_file_from_disk(file_path: str) -> None:
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.error(e, exc_info=True)
        raise IOError("Failed to delete file from disk") from e


def _get_file_content(file_path: str) -> bytes:
    try:
        with open(file_path, "rb") as f:
            return f.read()
    except Exception as e:
        logger.error(e, exc_info=True)
        raise IOError("Failed to read file from disk") from e


def _get_file_type(file_content: bytes, original_filename: str) -> str:
    """Detect MIME type using filetype library then fallback to mimetypes.

    Raises ValueError if type not allowed or cannot be determined.
    """
    try:
        kind = filetype.guess(file_content)
        mime = None
        if kind is not None:
            mime = kind.mime
        if mime is None:
            mime, _ = mimetypes.guess_type(original_filename)
        if not mime:
            raise ValueError("Could not determine file type")
        if mime not in ALLOWED_MIME_TYPES:
            raise ValueError(f"File type '{mime}' is not allowed")
        return mime
    except ValueError:
        raise
    except Exception as e:
        logger.error(e, exc_info=True)
        raise ValueError("Failed to determine file type") from e


def _validate_file_size(file_content: bytes, max_size_mb: int = MAX_FILE_SIZE_MB) -> None:
    size_bytes = len(file_content)
    threshold = max_size_mb * 1024 * 1024
    if size_bytes > threshold:
        raise ValueError(f"File size {size_bytes} exceeds {threshold} bytes")
