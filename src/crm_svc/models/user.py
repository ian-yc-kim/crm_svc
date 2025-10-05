import uuid
from sqlalchemy import Column, String

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<User(id={self.id})>"
