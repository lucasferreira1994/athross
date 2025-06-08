from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/documents", tags=["documents"])

def db_get():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Document)
def document_create(document: schemas.DocumentCreate, db: Session = Depends(db_get)):
    # Verifica se o hash já existe
    db_doc = db.query(models.Document).filter_by(hash=document.hash).first()
    if db_doc:
        raise HTTPException(status_code=400, detail="Document hash already exists")
    
    return crud.create_document(db, document)
