<<<<<<< HEAD
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from database import Base
=======
from sqlalchemy import Column, ForeignKey, Table, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from database import Base
import datetime
>>>>>>> 584054f2643d394146b28b1a7904c5d83a34115a

document_label = Table(
    'document_label',
    Base.metadata,
    Column('document_id', pgUUID(as_uuid=True), ForeignKey('documents.id'), primary_key=True),
<<<<<<< HEAD
    Column('label_id', pgUUID(as_uuid=True), ForeignKey('labels.id'), primary_key=True)
=======
    Column('label_id', pgUUID(as_uuid=True), ForeignKey('labels.id'), primary_key=True),
    Column('created_at', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_at', DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
>>>>>>> 584054f2643d394146b28b1a7904c5d83a34115a
)