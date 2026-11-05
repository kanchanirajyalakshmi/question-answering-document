
import uuid

from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    Text
)

from sqlalchemy.sql import func

from app.database import Base


class Document(Base):

    __tablename__ = "documents"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    original_filename = Column(
        String(255),
        nullable=False
    )

    stored_filename = Column(
        String(255),
        nullable=False,
        unique=True
    )

    file_path = Column(
        Text,
        nullable=False
    )

    file_type = Column(
        String(20),
        nullable=False
    )

    file_size = Column(
        Integer,
        nullable=False
    )

    status = Column(
        String(30),
        nullable=False,
        default="uploaded"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
