from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
import api.schemas.schema_document as schema_document
import models.model_document as model_document
import services.service_document as service_document

router = APIRouter(prefix="/documents", tags=["documents"])

def db_get():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schema_document.Document])
def list_all(db: Session = Depends(db_get)):
    return service_document.list_all(db)

@router.post("/", response_model=List[schema_document.Document])
def create(documents: List[schema_document.DocumentCreate], db: Session = Depends(db_get)):
    return service_document.get_and_update_or_create(db, documents)

@router.delete("/", response_model=List[schema_document.Document])
def delete_all(db: Session = Depends(db_get)):
    return service_document.delete_all(db)
