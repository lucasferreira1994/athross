from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
import api.schemas.schema_label as schema_label
import models.model_label as model_label


def label_create(db: Session, label: schema_label.LabelCreate):
    db_label = model_label.Label(name=label.key, value=label.value)
    db.add(db_label)
    db.commit()
    db.refresh(db_label)
    return db_label

def label_list(db: Session):
    return db.query(model_label.Label).order_by(model_label.Label.key).all()