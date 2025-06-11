from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
import api.schemas.schema_label as schema_label
import services.service_label as service_label

router = APIRouter(prefix="/labels", tags=["labels"])

def db_get():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schema_label.Label])
def list_all(db: Session = Depends(db_get)):
    return service_label.list_all(db)

@router.post("/", response_model=List[schema_label.Label])
def create(labels: List[schema_label.LabelCreate],  db: Session = Depends(db_get)):
    return service_label.get_or_create(db, labels)

@router.patch("/", response_model=List[schema_label.Label])
def update(labels: List[schema_label.LabelCreate],  db: Session = Depends(db_get)):
    return service_label.patch(db, labels)

@router.delete("/{label_id}", response_model=schema_label.Label)
def delete(label_id: UUID4, db: Session = Depends(db_get)):
    return service_label.delete(db, label_id)

