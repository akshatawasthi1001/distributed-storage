import uuid

from sqlalchemy import (
    Column,
    String,
    BigInteger,
    DateTime,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    filename = Column(
        String,
        nullable=False
    )

    owner_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    storage_path = Column(
        String,
        nullable=False
    )

    size = Column(BigInteger)

    current_version = Column(
        BigInteger,
        default=1
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    owner = relationship(
        "User",
        back_populates="files"
    )

    versions = relationship(
        "FileVersion",
        back_populates="file",
        cascade="all, delete-orphan"
    )   