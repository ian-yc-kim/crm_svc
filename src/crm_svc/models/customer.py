import uuid
from sqlalchemy import Column, String

from .base import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Customer(id={self.id})>"
