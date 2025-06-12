from sqlalchemy.orm import Session, joinedload

import uuid
import json

import models.model_document as model_document
import models.model_label as model_label
import api.schemas.schema_document as schema_document
import api.schemas.schema_document_type as schema_document_type
import api.schemas.schema_label as schema_label
import services.service_document_type as service_document_type

def list_all(db: Session):
    response = []
    for document in db.query(model_document.Document).options(joinedload(model_document.Document.labels)).all():
        response.append(
            schema_document.Document(
                id=document.id,
                hash=document.hash,
                type=schema_document_type.DocumentType(
                    id=document.type.id,
                    name=document.type.name,
                    created_at=document.type.created_at,
                    updated_at=document.type.updated_at
                ),
                created_by=document.created_by,
                document=json.loads(document.document),
                labels=[
                    schema_label.Label(
                        id=label.id,
                        key=label.key,
                        value=label.value,
                        created_at=label.created_at,
                        updated_at=label.updated_at
                    )
                    for label in document.labels
                ],
                labels_string=document.labels_string,
                created_at=document.created_at,
                updated_at=document.updated_at
            )
        )
    return response
    

def get_and_update_or_create(db: Session, doc_data: schema_document.DocumentCreate):
    documents_response = []

    for doc in doc_data:
        # Get or create document type
        document_type_obj = schema_document_type.DocumentTypeBase(name=doc.type)
        document_type = service_document_type.get_or_create(db, [document_type_obj])[0]

        # Vefiry if document already exists
        existing_document = db.query(model_document.Document).filter(
            model_document.Document.hash == doc.hash
        ).first()

        if existing_document:
            # Update
            existing_document.type_id = document_type.id
            existing_document.created_by = doc.created_by
            existing_document.document = json.dumps(doc.document)
            documento_to_update = existing_document
        else:
            # Create new
            documento_to_update = model_document.Document(
                hash=doc.hash,
                type_id=document_type.id,
                created_by=doc.created_by,
                document=json.dumps(doc.document),
            )
            db.add(documento_to_update)
            db.flush()  # Make ID and relationship available before commit

        # Update labels
        documento_to_update.labels.clear()  # Remove existing labels

        for label in doc.labels:
            existing_label = db.query(model_label.Label).filter(
                model_label.Label.key == label.key,
                model_label.Label.value == label.value
            ).first()

            if not existing_label:
                # Cria label nova
                existing_label = model_label.Label(
                    key=label.key,
                    value=label.value
                )
                db.add(existing_label)
                db.flush()

            documento_to_update.labels.append(existing_label)
        

        db.flush()
        db.commit()
        db.refresh(documento_to_update)
        documents_response.append(documento_to_update)

    # Mount response
    response = []
    for document in documents_response:
        document = db.query(model_document.Document).options(
            joinedload(model_document.Document.labels)
        ).filter(
            model_document.Document.id == document.id
        ).first()
        response.append(
            schema_document.Document(
                id=document.id,
                hash=document.hash,
                type=schema_document_type.DocumentType(
                    id=document.type.id,
                    name=document.type.name,
                    created_at=document.type.created_at,
                    updated_at=document.type.updated_at
                ),
                created_by=document.created_by,
                document=json.loads(document.document),
                labels=[
                    schema_label.Label(
                        id=label.id,
                        key=label.key,
                        value=label.value,
                        created_at=label.created_at,
                        updated_at=label.updated_at
                    )
                    for label in document.labels
                ],
                labels_string=document.labels_string,
                created_at=document.created_at,
                updated_at=document.updated_at
            )
        )
    return response

def delete(db: Session, id: uuid.UUID):
    db.query(model_document.Document).filter(model_document.Document.id == id).delete()
    db.commit()

def delete_all(db: Session):
    db.query(model_document.Document).delete()
    db.commit()
