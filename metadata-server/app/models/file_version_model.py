import uuid

from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class FileVersion(Base):
    __tablename__ = "file_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    file_id = Column(
        UUID(as_uuid=True),
        ForeignKey("files.id", ondelete="CASCADE"),
        nullable=False
    )

    version = Column(Integer, nullable=False)

    storage_path = Column(String, nullable=False)

    size = Column(BigInteger, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    file = relationship(
        "File",
        back_populates="versions"
    )