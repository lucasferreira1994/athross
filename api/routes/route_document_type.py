from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
import api.schemas.schema_document_type as schema_document_type
import services.service_document_type as service_document_type

router = APIRouter(prefix="/document-types", tags=["document-types"])

def db_get():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schema_document_type.DocumentType])
def list_all(db: Session = Depends(db_get)):
    return service_document_type.list_all(db)

@router.post("/", response_model=List[schema_document_type.DocumentType])
def create(document_types: List[schema_document_type.DocumentTypeCreate], db: Session = Depends(db_get)):
    return service_document_type.get_or_create(db, document_types)

@router.patch("/", response_model=List[schema_document_type.DocumentType])
def update(document_types: List[schema_document_type.DocumentTypeCreate], db: Session = Depends(db_get)):
    return service_document_type.patch(db, document_types)

@router.delete("/{document_type_id}", response_model=schema_document_type.DocumentType)
def delete(document_type_id: UUID4, db: Session = Depends(db_get)):
    return service_document_type.delete(db, document_type_id)


