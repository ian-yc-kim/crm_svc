from datetime import datetime
from sqlalchemy import select

from crm_svc.models import Document


def test_create_and_query_document(db_session):
    doc = Document(
        id="doc-1",
        customer_id="cust-1",
        uploaded_by_user_id="user-1",
        original_filename="orig.pdf",
        stored_filename="stored_1.pdf",
        file_path="/tmp/stored_1.pdf",
        file_type="application/pdf",
        file_size=1234,
        uploaded_at=datetime.utcnow(),
        virus_scan_status="PENDING",
        access_level="PRIVATE",
        metadata_json={"key": "value"},
    )

    try:
        db_session.add(doc)
        db_session.commit()
    except Exception as e:
        import logging

        logging.error(e, exc_info=True)
        raise

    stmt = select(Document).where(Document.stored_filename == "stored_1.pdf")
    result = db_session.execute(stmt).scalars().one()

    assert result.original_filename == "orig.pdf"
    assert result.metadata_json["key"] == "value"
