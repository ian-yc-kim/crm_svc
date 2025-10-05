from enum import Enum
from typing import Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class VirusScanStatus(str, Enum):
    PENDING = "PENDING"
    CLEAN = "CLEAN"
    INFECTED = "INFECTED"


class DocumentCreate(BaseModel):
    # Use string IDs to align with how IDs are stored and tests expect
    customer_id: str
    uploaded_by_user_id: str
    access_level: str
    metadata: Optional[Dict] = None


class DocumentResponse(BaseModel):
    # Present IDs as strings so callers/tests can safely call uuid.UUID(resp.id)
    id: str
    customer_id: str
    uploaded_by_user_id: str
    original_filename: str
    stored_filename: str
    file_path: str
    file_type: str
    file_size: int
    uploaded_at: datetime
    virus_scan_status: VirusScanStatus
    access_level: str
    metadata: Optional[Dict] = Field(default=None, alias="metadata_json")

    model_config = {"from_attributes": True}
