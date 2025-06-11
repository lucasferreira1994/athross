from pydantic import BaseModel, UUID4, ConfigDict
from typing import List, Optional
from datetime import datetime

class LabelBase(BaseModel):
    key: str
    value: str

class LabelCreate(LabelBase):
    pass

class LabelDelete(BaseModel):
    id: UUID4

class Label(LabelBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        model_config = ConfigDict(from_attributes=True)
