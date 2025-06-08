from sqlalchemy import Column, String, DateTime, ForeignKey, Table, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from ..database import Base

# Tabela de associação para labels
document_label = Table(
    'document_label', Base.metadata,
    Column('document_id', ForeignKey('documents.id'), primary_key=True),
    Column('label_id', ForeignKey('labels.id'), primary_key=True)
)

class Label(Base):
    __tablename__ = 'labels'

    id = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    value = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint('name', 'value', name='_name_value_uc'),)