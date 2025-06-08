from pydantic import BaseModel, UUID4
from typing import List, Optional
from datetime import datetime

class LabelBase(BaseModel):
    name: str
    value: str

class LabelCreate(LabelBase):
    pass

class Label(LabelBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class DocumentTypeBase(BaseModel):
    name: str

class DocumentTypeCreate(DocumentTypeBase):
    pass

class DocumentType(DocumentTypeBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class DocumentBase(BaseModel):
    hash: str
    created_by: str
    labels_string: Optional[str]
    document: Optional[dict] = {}

class DocumentCreate(DocumentBase):
    type_id: UUID4
    label_ids: List[UUID4] = []

class Document(DocumentBase):
    id: UUID4
    type: DocumentType
    labels: List[Label]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
