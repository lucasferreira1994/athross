from sqlalchemy import Column, String, DateTime, ForeignKey, Table, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from database import Base
from models.model_relationship import document_label

class Label(Base):
    __tablename__ = 'labels'

    id = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    documents = relationship(
        "Document",
        secondary=document_label,
        back_populates='labels'
    )

    __table_args__ = (UniqueConstraint('key', 'value', name='_name_value_uc'),)