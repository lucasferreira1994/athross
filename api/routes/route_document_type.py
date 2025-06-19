from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import api.schemas.schema_document_type as schema_document_type
import services.service_document_type as service_document_type
from factory.factory_database import get_async_db
from api.schemas.schema_paginator import PaginatedResponse
from fastapi import Query
from typing import Optional

router = APIRouter(prefix="/api/v1/document-types", tags=["document-types"])

@router.get("/", response_model=PaginatedResponse[schema_document_type.DocumentType])
async def list_all(
    db: AsyncSession = Depends(get_async_db),
    skip: Optional[int] = Query(0, alias="offset", ge=0),
    limit: Optional[int] = Query(100, le=1000)
):
    items, total = await service_document_type.list_all(db, skip=skip, limit=limit)
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.post("/", response_model=List[schema_document_type.DocumentType])
async def create(
    document_types: List[schema_document_type.DocumentTypeCreate], 
    db: AsyncSession = Depends(get_async_db)
):
    response = await service_document_type.get_or_create(db, document_types)
    return response

@router.patch("/", response_model=List[schema_document_type.DocumentType])
async def update(
    document_types: List[schema_document_type.DocumentTypeCreate], 
    db: AsyncSession = Depends(get_async_db)
):
    response = await service_document_type.patch(db, document_types)
    return response

@router.delete("/{document_type_id}", response_model=schema_document_type.DocumentType)
async def delete(
    document_type_id: UUID4, 
    db: AsyncSession = Depends(get_async_db)
):
    response = await service_document_type.delete(db, document_type_id)
    return response