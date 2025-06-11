from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models.model_label as model_label
import api.schemas.schema_label as schema_label

def list_all(db: Session):
    return db.query(model_label.Label).order_by(model_label.Label.key).all()

def get_or_create(db: Session, labels: List[schema_label.LabelCreate]):
    input_keys = [label.key for label in labels]

    # 1. get all labels with the same key=value
    existing_labels = db.query(model_label.Label)\
        .filter(model_label.Label.key.in_(input_keys))\
        .all()

    existing_keys = {label.key for label in existing_labels}

    # 2. create new labels
    new_labels = []
    for label in labels:
        if label.key not in existing_keys:
            new_label = model_label.Label(key=label.key, value=label.value)
            db.add(new_label)
            new_labels.append(new_label)

    if new_labels:
        db.commit()
        for label in new_labels:
            db.refresh(label)

    # 3. return all labels
    return existing_labels + new_labels

def delete(db: Session, label_id: schema_label.LabelDelete):
    existing_labels = db.query(model_label.Label).filter(model_label.Label.id == label_id).first()
    if not existing_labels:
        raise HTTPException(status_code=404, detail="Label not found")
    db.delete(existing_labels)
    db.commit()
    return existing_labels