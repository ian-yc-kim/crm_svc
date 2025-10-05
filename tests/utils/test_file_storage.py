import io
import uuid
import os
import pytest

from crm_svc.utils.file_storage import (
    _save_file_to_disk,
    _get_file_content,
    _delete_file_from_disk,
    _validate_file_size,
    _get_file_type,
)
from crm_svc import config


def test_save_get_delete_happy_path(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DOCUMENT_STORAGE_PATH", str(tmp_path))
    # PNG header bytes
    content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
    original_filename = "image.png"
    customer_id = uuid.uuid4()

    stored_filename, file_path = _save_file_to_disk(content, original_filename, customer_id)
    assert os.path.exists(file_path)

    read = _get_file_content(file_path)
    assert read == content

    _delete_file_from_disk(file_path)
    assert not os.path.exists(file_path)


def test_validate_file_size_raises():
    big = b"0" * (11 * 1024 * 1024)
    with pytest.raises(ValueError):
        _validate_file_size(big, max_size_mb=10)


def test_get_file_type_rejects(monkeypatch):
    # plain text should be rejected
    content = b"hello world"
    with pytest.raises(ValueError):
        _get_file_type(content, "file.txt")
