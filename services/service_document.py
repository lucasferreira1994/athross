from sqlalchemy.orm import Session
import uuid

import models.model_document as model_document
import models.model_label as model_label
import api.schemas.schema_document as schema_document



def document_create(db: Session, doc_data: schema_document.DocumentCreate):
    db_doc = models.Document(
        id=uuid.uuid4(),
        hash=doc_data.hash,
        type_id=doc_data.type_id,
        created_by=doc_data.created_by,
        document=doc_data.document,
        labels_string=doc_data.labels_string
    )
    if doc_data.label_ids:
        labels = db.query(models.Label).filter(models.Label.id.in_(doc_data.label_ids)).all()
        db_doc.labels.extend(labels)

    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc