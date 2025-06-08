from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import SessionLocal

def document_type_create(db: Session, data: schemas.DocumentTypeCreate):
    db_type = models.DocumentType(name=data.name)
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    return db_type

def documenttype_list(db: Session):
    return db.query(models.DocumentType).order_by(models.DocumentType.name).all()