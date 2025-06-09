from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
import api.schemas.schema_document_type as schema_document_type
import models.model_document_type as model_document_type

def document_type_create(db: Session, data: schema_document_type.DocumentTypeCreate):
    db_type = model_document_type.DocumentType(name=data.name)
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    return db_type

def documenttype_list(db: Session):
    return db.query(model_document_type.DocumentType).order_by(model_document_type.DocumentType.name).all()