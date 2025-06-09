from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import SessionLocal


def label_create(db: Session, label: schemas.LabelCreate):
    db_label = models.Label(name=label.name, value=label.value)
    db.add(db_label)
    db.commit()
    db.refresh(db_label)
    return db_label

def label_list(db: Session):
    return db.query(models.Label).order_by(models.Label.name).all()