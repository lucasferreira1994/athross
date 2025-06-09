from pydantic import BaseModel, UUID4
from typing import List, Optional
from datetime import datetime

class LabelBase(BaseModel):
    key: str
    value: str

class LabelCreate(LabelBase):
    pass

class Label(LabelBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
