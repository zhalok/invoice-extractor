import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB

from db import Base


def _uuid() -> str:
    return str(uuid.uuid4())


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    filename = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)

    status = Column(String, nullable=False, default="queued")

    extracted = Column(JSONB, nullable=True)
    verification = Column(JSONB, nullable=True)
    registration = Column(JSONB, nullable=True)
    error = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), default=_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=_now, onupdate=_now, nullable=False)
