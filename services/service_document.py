import uuid
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import delete as sa_delete
from typing import List
import models.model_document as model_document
import models.model_label as model_label
import models.model_relationship as model_relationship
import api.schemas.schema_document as schema_document
import api.schemas.schema_document_type as schema_document_type
import api.schemas.schema_label as schema_label
import services.service_document_type as service_document_type
from models.model_document_type import DocumentType
import datetime

async def list_all(db: AsyncSession) -> List[schema_document.Document]:
    response = []

    result = await db.execute(
        select(model_document.Document)
        .options(joinedload(model_document.Document.labels), joinedload(model_document.Document.type))
    )
    documents = result.unique().scalars().all()

    for document in documents:
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



async def create_or_update_documents(db: AsyncSession, documents_data: list):
    for doc_data in documents_data:
        doc_type = await db.scalar(select(DocumentType).filter_by(name=doc_data.type))
        if not doc_type:
            doc_type = DocumentType(name=doc_data.type)
            db.add(doc_type)
            await db.flush()

        existing_doc = await db.scalar(select(model_document.Document).filter_by(hash=doc_data.hash))

        label_objs = []
        for label in doc_data.labels or []:
            label_obj = await db.scalar(
                select(model_label.Label).filter_by(key=label.key, value=label.value)
            )
            if not label_obj:
                label_obj = model_label.Label(key=label.key, value=label.value)
                db.add(label_obj)
                await db.flush()
            label_objs.append(label_obj)

        label_objs = list(set(label_objs))

        if existing_doc:

            existing_doc.type_id = doc_type.id
            existing_doc.created_by = doc_data.created_by
            existing_doc.document = json.dumps(doc_data.document or {})

            # clear labels on input?
            LABELS_CLEAR_ON_INPUT = False
            if LABELS_CLEAR_ON_INPUT:
                existing_doc.labels.clear()
            
            # evict already existing labels to document
            labels_to_add = label_objs
            labels_to_add = [label for label in label_objs if label not in existing_doc.labels]
            if labels_to_add:
                existing_doc.labels.extend(labels_to_add)
                

            document = existing_doc
        else:
            new_doc = model_document.Document(
                hash=doc_data.hash,
                type_id=doc_type.id,
                created_by=doc_data.created_by,
                document=json.dumps(doc_data.document or {}),
                labels=label_objs,
            )
            db.add(new_doc)

            document = new_doc
        
        for label in label_objs:
            await db.execute(
                model_relationship.document_label.update().where(
                    model_relationship.document_label.c.document_id == document.id,
                    model_relationship.document_label.c.label_id == label.id
                ).values(
                    updated_at=datetime.datetime.utcnow()
                )
            )

    await db.commit()

    response = await list_all(db)
    return response

async def delete(db: AsyncSession, id: uuid.UUID):
    await db.execute(
        sa_delete(model_document.Document).where(model_document.Document.id == id)
    )
    await db.commit()


async def delete_all(db: AsyncSession):
    await db.execute(sa_delete(model_document.Document))
    await db.commit()
    return