from pydantic import BaseModel, UUID4, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from api.schemas.schema_document_type import DocumentType
from .schema_label import Label

class DocumentBase(BaseModel):
    hash: str
    created_by: str
    labels_string: Optional[str]
    document: Optional[dict] = Field(default_factory=dict)

class DocumentCreate(DocumentBase):
    type_id: UUID4
    label_ids: List[UUID4] = []

class Document(DocumentBase):
    id: UUID4
    type: DocumentType
    labels: List[Label]
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        model_config = ConfigDict(from_attributes=True)
