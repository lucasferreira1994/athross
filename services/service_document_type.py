from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Tuple
import api.schemas.schema_document_type as schema_document_type
import models.model_document_type as model_document_type
from sqlalchemy import func


async def list_all(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100
) -> Tuple[List[model_document_type.DocumentType], int]:
    items_result = await db.execute(
        select(model_document_type.DocumentType)
        .order_by(model_document_type.DocumentType.name)
        .offset(skip)
        .limit(limit)
    )
    items = items_result.scalars().all()
    
    count_result = await db.execute(
        select(func.count()).select_from(model_document_type.DocumentType)
    )
    total = count_result.scalar_one()
    
    return items, total

async def get_or_create(
        db: AsyncSession, 
        document_types: List[schema_document_type.DocumentTypeCreate]
    ) -> List[model_document_type.DocumentType]:

    input_types = [document_type.name for document_type in document_types]

    result = await db.execute(
        select(model_document_type.DocumentType)
        .where(model_document_type.DocumentType.name.in_(input_types))
    )
    existing_document_types = result.scalars().all()
    existing_keys = {document_type.name for document_type in existing_document_types}

    new_document_types = []
    for document_type in document_types:
        if document_type.name not in existing_keys:
            new_document_type = model_document_type.DocumentType(name=document_type.name)
            db.add(new_document_type)
            new_document_types.append(new_document_type)

    if new_document_types:
        await db.commit()
        for document_type in new_document_types:
            await db.refresh(document_type)

    return existing_document_types + new_document_types

async def delete(db: AsyncSession, document_type_id: UUID4):
    result = await db.execute(
        select(model_document_type.DocumentType)
        .where(model_document_type.DocumentType.id == document_type_id)
    )
    existing_document_type = result.scalars().first()
    
    if not existing_document_type:
        raise HTTPException(status_code=404, detail="DocumentType not found")
    
    await db.delete(existing_document_type)
    await db.commit()
    return existing_document_type