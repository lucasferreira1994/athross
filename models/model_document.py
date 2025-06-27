from sqlalchemy import Column, String, DateTime, ForeignKey, event
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import relationship, Session
from datetime import datetime
import uuid
from sqlalchemy import JSON as dbJson
from database import Base
import models.model_label as model_label
from models.model_relationship import document_label

class Document(Base):
    __tablename__ = 'documents'

    id = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hash = Column(String, unique=True, nullable=False)
    type_id = Column(pgUUID(as_uuid=True), ForeignKey('document_types.id'), nullable=False)
    created_by = Column(String, nullable=False)
    document = Column(dbJson, nullable=True, default={})
    labels_string = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    type = relationship("DocumentType")
    labels = relationship("Label", secondary=document_label, back_populates="documents", lazy="joined")

def generate_labels_string(labels):
    return ",".join([f"{label.key}={label.value}" for label in labels])


@event.listens_for(Session, "before_flush")
def update_labels_string(session, flush_context, _):
    for instance in session.new.union(session.dirty):
        if isinstance(instance, Document):
            new_value = generate_labels_string(instance.labels or [])
            if instance.labels_string != new_value:
                instance.labels_string = new_value