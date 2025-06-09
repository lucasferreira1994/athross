from sqlalchemy import Column, String, DateTime, ForeignKey, Table, Enum, and_
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from database import Base
import models.model_label  as model_label


class LabelType(enum.Enum):
    input = 'input'
    rules = 'rules'

document_label = Table(
    'document_label',
    Base.metadata,
    Column('document_id', pgUUID(as_uuid=True), ForeignKey('documents.id'), primary_key=True),
    Column('label_id', pgUUID(as_uuid=True), ForeignKey('labels.id'), primary_key=True),
    Column('type', Enum(LabelType, name='label_type_enum'), nullable=False)
)

class Document(Base):
    __tablename__ = 'documents'

    id = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hash = Column(String, unique=True, nullable=False)
    type_id = Column(pgUUID(as_uuid=True), ForeignKey('document_types.id'), nullable=False)
    created_by = Column(String, nullable=False)
    document = Column(String, nullable=True)
    labels_string = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    type = relationship("DocumentType")

    labels = relationship(
        model_label.Label,
        secondary=document_label,
        back_populates="documents"
    )

