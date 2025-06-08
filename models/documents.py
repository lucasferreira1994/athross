from sqlalchemy import Column, String, DateTime, ForeignKey, Table, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from ..database import Base

class Document(Base):
    __tablename__ = 'documents'

    id = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hash = Column(String, unique=True, nullable=False)
    type_id = Column(pgUUID(as_uuid=True), ForeignKey('document_types.id'), nullable=False)
    created_by = Column(String, nullable=False)
    document = Column(String, nullable=True)  # ou JSON, dependendo do banco
    labels_string = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    type = relationship("DocumentType")
    labels = relationship("Label", secondary=document_label)
