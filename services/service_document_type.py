from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
import api.schemas.schema_document_type as schema_document_type
import models.model_document_type as model_document_type

def list_all(db: Session):
    return db.query(model_document_type.DocumentType).order_by(model_document_type.DocumentType.name).all()

def get_or_create(db: Session, document_types: List[schema_document_type.DocumentTypeCreate]):
    input_types= [document_type.name for document_type in document_types]

    # 1. get all document_type with name
    existing_document_types = db.query(model_document_type.DocumentType)\
        .filter(model_document_type.DocumentType.name.in_(input_types))\
        .all()

    existing_keys = {document_type.name for document_type in existing_document_types}

    # 2. create new document_type
    new_document_types = []
    for document_type in document_types:
        if document_type.name not in existing_keys:
            new_document_type = model_document_type.DocumentType(name=document_type.name)
            db.add(new_document_type)
            new_document_types.append(new_document_type)

    if new_document_types:
        db.commit()
        for document_type in new_document_types:
            db.refresh(document_type)

    # 3. return all document_type
    return existing_document_types + new_document_types

def delete(db: Session, document_type_id: UUID4):
    existing_document_type = db.query(model_document_type.DocumentType).filter(model_document_type.DocumentType.id == document_type_id).first()
    if not existing_document_type:
        raise HTTPException(status_code=404, detail="DocumentType not found")
    db.delete(existing_document_type)
    db.commit()
    return existing_document_type


    