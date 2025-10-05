import io
import uuid
import os
import pytest
from starlette.datastructures import UploadFile

from crm_svc.services.document_service import DocumentService
from crm_svc import config
from crm_svc.models import Customer, User


def make_uploadfile(content: bytes, filename: str, content_type: str = None) -> UploadFile:
    stream = io.BytesIO(content)
    # Construct using keyword arguments to match UploadFile signature
    up = UploadFile(file=stream, filename=filename)
    if content_type:
        try:
            up.content_type = content_type
        except Exception:
            # If setting content_type is not supported, ignore
            pass
    return up


def test_upload_metadata_download_delete_flow(tmp_path, monkeypatch, db_session):
    monkeypatch.setattr(config, "DOCUMENT_STORAGE_PATH", str(tmp_path))

    svc = DocumentService()

    # create customer and user
    customer = Customer(id=str(uuid.uuid4()))
    user = User(id=str(uuid.uuid4()))
    db_session.add(customer)
    db_session.add(user)
    db_session.commit()

    # PNG-like content
    content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
    f = make_uploadfile(content, "photo.png", "image/png")

    resp = svc.upload_document(db_session, uuid.UUID(customer.id), uuid.UUID(user.id), f, access_level="PRIVATE", metadata={"a":1})
    assert resp.original_filename == "photo.png"
    assert resp.file_type == "image/png"
    assert os.path.exists(resp.file_path)

    # download
    data, orig_name, mime = svc.download_document(db_session, uuid.UUID(resp.id))
    assert data == content
    assert orig_name == "photo.png"
    assert mime == "image/png"

    # metadata
    meta = svc.get_document_metadata(db_session, uuid.UUID(resp.id))
    assert meta.id == resp.id

    # list by customer
    lst = svc.list_documents_for_customer(db_session, uuid.UUID(customer.id))
    assert any(d.id == resp.id for d in lst)

    # delete
    svc.delete_document(db_session, uuid.UUID(resp.id))
    # ensure deleted from db
    with pytest.raises(Exception):
        svc.get_document_metadata(db_session, uuid.UUID(resp.id))
    # file should be gone
    assert not os.path.exists(resp.file_path)


def test_upload_invalid_type_and_size(monkeypatch, tmp_path, db_session):
    monkeypatch.setattr(config, "DOCUMENT_STORAGE_PATH", str(tmp_path))
    svc = DocumentService()

    customer = Customer(id=str(uuid.uuid4()))
    user = User(id=str(uuid.uuid4()))
    db_session.add(customer)
    db_session.add(user)
    db_session.commit()

    # invalid type
    txt = b"just text"
    f_txt = UploadFile(file=io.BytesIO(txt), filename="notes.txt")
    with pytest.raises(Exception):
        svc.upload_document(db_session, uuid.UUID(customer.id), uuid.UUID(user.id), f_txt, access_level="PRIVATE", metadata=None)

    # oversized
    big = b"0" * (11 * 1024 * 1024)
    f_big = UploadFile(file=io.BytesIO(big), filename="big.pdf")
    with pytest.raises(Exception):
        svc.upload_document(db_session, uuid.UUID(customer.id), uuid.UUID(user.id), f_big, access_level="PRIVATE", metadata=None)


def test_not_found_edge_cases(db_session):
    svc = DocumentService()
    random_id = uuid.uuid4()
    with pytest.raises(Exception):
        svc.get_document_metadata(db_session, random_id)
    with pytest.raises(Exception):
        svc.download_document(db_session, random_id)
    with pytest.raises(Exception):
        svc.delete_document(db_session, random_id)
