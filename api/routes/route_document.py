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
def document_list(db: Session = Depends(db_get)):
    return db.query(model_document.Document).all()

@router.post("/", response_model=schema_document.Document)
def document_create(document: schema_document.DocumentCreate, db: Session = Depends(db_get)):
    # Verifica se o hash já existe
    db_doc = db.query(model_document.Document).filter_by(hash=document.hash).first()
    if db_doc:
        raise HTTPException(status_code=400, detail="Document hash already exists")
    
    return service_document.create_document(db, document)

