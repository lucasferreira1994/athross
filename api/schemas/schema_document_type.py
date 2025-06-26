from pydantic import BaseModel, UUID4, ConfigDict
from typing import List, Optional
from datetime import datetime

class DocumentTypeBase(BaseModel):
    name: str

class DocumentTypeCreate(DocumentTypeBase):
    pass

class DocumentType(DocumentTypeBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        model_config = ConfigDict(from_attributes=True)