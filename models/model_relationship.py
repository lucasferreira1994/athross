from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from database import Base

document_label = Table(
    'document_label',
    Base.metadata,
    Column('document_id', pgUUID(as_uuid=True), ForeignKey('documents.id'), primary_key=True),
    Column('label_id', pgUUID(as_uuid=True), ForeignKey('labels.id'), primary_key=True)
)