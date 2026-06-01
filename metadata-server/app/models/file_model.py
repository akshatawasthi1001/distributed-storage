import uuid

from sqlalchemy import Column, String, BigInteger
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base

class File(Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    filename = Column(String, nullable=False)

    storage_path = Column(String, nullable=False)

    size = Column(BigInteger)