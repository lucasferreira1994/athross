from pydantic import BaseModel, UUID4, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from api.schemas.schema_document_type import DocumentType
from .schema_label import LabelBase, Label

class DocumentBase(BaseModel):
    hash: str
    labels_string: Optional[str] = None
    document: Optional[dict] = Field(default_factory=dict)

    class ConfigDict:
        model_config = ConfigDict(from_attributes=True)

class Document(DocumentBase):
    id: UUID4
    hash: str
    type: DocumentType
    labels: List[Label]
    created_by: str
    document: dict
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        model_config = ConfigDict(from_attributes=True)

class DocumentCreate(DocumentBase):
    type: str
    created_by: str
    labels: List[LabelBase]
    class ConfigDict:
        model_config = ConfigDict(from_attributes=True)
