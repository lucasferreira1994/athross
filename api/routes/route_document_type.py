from fastapi import APIRouter, Depends, Query, status, Cookie, HTTPException
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import api.schemas.schema_document_type as schema_document_type
import repository.repository_document_type as repository_document_type
from factory.factory_database import get_async_db
from api.schemas.schema_paginator import PaginatedResponse
from services import service_auth


router = APIRouter(
    prefix="/document-types",
    tags=["Document Types"],
    responses={
        400: {"description": "Invalid input data"},
        404: {"description": "Document type not found"},
        422: {"description": "Validation error in request parameters"}
    }
)

@router.get(
    "/",
    response_model=PaginatedResponse[schema_document_type.DocumentType],
    status_code=status.HTTP_200_OK,
    summary="List all document types",
    description="Retrieves a paginated list of document types with metadata about the collection.",
    response_description="Paginated response containing document types and collection metadata"
)
async def list_all(
    db: AsyncSession = Depends(get_async_db),
    skip: Optional[int] = Query(
        0,
        alias="offset",
        ge=0,
        description="Number of items to skip for pagination"
    ),
    limit: Optional[int] = Query(
        100,
        le=1000,
        description="Maximum number of items to return (up to 1000)"
    ),
    access_token: str | None = Cookie(default=None)

):
    user = await service_auth.get_user_by_token(db, access_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User Not Found or Inactive"
        )
    
    items, total = await repository_document_type.list_all(db, skip=skip, limit=limit)
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@router.post(
    "/",
    response_model=List[schema_document_type.DocumentType],
    status_code=status.HTTP_201_CREATED,
    summary="Create document types",
    description="Creates one or multiple document types. If a document type already exists, returns the existing record.",
    response_description="List of created or existing document types"
)
async def create(
    document_types: List[schema_document_type.DocumentTypeCreate],
    db: AsyncSession = Depends(get_async_db),
    access_token: str | None = Cookie(default=None)
):
    user = await service_auth.get_user_by_token(db, access_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User Not Found or Inactive"
        )
    response = await repository_document_type.get_or_create(db, document_types)
    return response

@router.patch(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[schema_document_type.DocumentType],
    summary="Update document types",
    description="Updates one or multiple document types. Types are matched by their names.",
    response_description="List of updated document types",
    responses={
        404: {"description": "One or more document types not found"}
    }
)
async def update(
    document_types: List[schema_document_type.DocumentTypeCreate],
    db: AsyncSession = Depends(get_async_db),
    access_token: str | None = Cookie(default=None)
):
    user = await service_auth.get_user_by_token(db, access_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User Not Found or Inactive"
        )
    response = await repository_document_type.patch(db, document_types)
    return response

@router.delete(
    "/{document_type_id}",
    status_code=status.HTTP_200_OK,
    response_model=schema_document_type.DocumentType,
    summary="Delete a document type",
    description="Deletes a specific document type by its unique identifier.",
    response_description="The deleted document type object",
    responses={
        200: {"description": "Document type successfully deleted"},
        404: {"description": "Document type not found with the specified ID"}
    }
)
async def delete(
    document_type_id: UUID4,
    db: AsyncSession = Depends(get_async_db),
    access_token: str | None = Cookie(default=None)
):
    
    user = await service_auth.get_user_by_token(db, access_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User Not Found or Inactive"
        )
    response = await repository_document_type.delete(db, document_type_id)
    return response