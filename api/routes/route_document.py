<<<<<<< HEAD
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid
import repository.repository_document as repository_document
from factory.factory_database import get_async_db
from services import services_label
from repository import repository_label
from api.schemas import schema_document, schema_search

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
    responses={
        400: {"description": "Bad request"},
        500: {"description": "Internal server error"}
    }
)

@router.get(
    "/",
    response_model=List[schema_document.Document],
    summary="List all documents",
    description="Retrieves a complete list of all documents in the system.",
    response_description="List of document objects with full details",
    responses={
        200: {
            "description": "Successful operation",
            "content": {
                "application/json": {
                    "example": [{
                        "id": "doc_123",
                        "title": "Sample Document",
                        "content": "Content demo...",
                        "type_id": "type_456"
                    }]
                }
            }
        }
    }
)
async def list_all(db: AsyncSession = Depends(get_async_db)):
    response = await repository_document.list_all(db)
    return response

@router.post(
    "/",
    response_model=List[schema_document.Document],
    status_code=status.HTTP_201_CREATED,
    summary="Create or update documents",
    description="Creates new documents or updates existing ones in bulk operation.",
    response_description="List of created/updated document objects",
    responses={
        201: {
            "description": "Documents successfully created/updated",
            "content": {
                "application/json": {
                    "example": [{
                        "id": "doc_123",
                        "title": "Updated Document",
                        "content": "New content...",
                        "type_id": "type_456"
                    }]
                }
            }
        },
        400: {
            "description": "Invalid input data",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid document format"}
                }
            }
        }
    }
)
=======
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_async_db
import api.schemas.schema_document as schema_document
import services.service_document as service_document

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])


@router.get("/", response_model=List[schema_document.Document])
async def list_all(db: AsyncSession = Depends(get_async_db)):
    response = await service_document.list_all(db)
    return response


@router.post("/", response_model=List[schema_document.Document])
>>>>>>> 584054f2643d394146b28b1a7904c5d83a34115a
async def create(
    documents: List[schema_document.DocumentCreate],
    db: AsyncSession = Depends(get_async_db)
):
<<<<<<< HEAD

    response = await repository_document.create_or_update_documents(db, documents)
    return response

@router.delete(
    "/",
    response_model=None,
    summary="Delete all documents",
    description="Permanently removes all documents from the system. Use with extreme caution!",
    response_description="Confirmation message",
    responses={
        200: {
            "description": "Successful deletion",
            "content": {
                "application/json": {
                    "example": {"detail": "All documents deleted"}
                }
            }
        },
        403: {
            "description": "Operation not permitted",
            "content": {
                "application/json": {
                    "example": {"detail": "Not authorized for this operation"}
                }
            }
        }
    }
)
async def delete_list(db: AsyncSession = Depends(get_async_db), raw_documents: List[str] = []):

    if not raw_documents:
        raise HTTPException(status_code=404, detail="Missing document UUIDs")
    
    documents_uuid = [uuid.UUID(document_uuid) for document_uuid in raw_documents]
    await repository_document.delete_by_uuids(db, documents_uuid)
    return JSONResponse({"detail": "All documents deleted"}, status_code=200)


@router.post(
    "/search",
    response_model=schema_search.DocumentSearchResponse,
    summary="Search for documents by labels",
    description="""
    This endpoint allows searching for documents based on the provided labels, and returns associated metadata and derived relationships.

    The response format depends on the by_type parameter:

    - If by_type = False: the documents will be returned in a flat list under the documents field.

    - If by_type = True: the documents will be grouped by type in a dictionary under the documents_by_type field.
""",
    responses={
        200: {
            "description": "Successful operation",
            "content": {
                "application/json": {
                    "examples": {
                        "flat_response": {
                            "summary": "Response with (by_type=False)",
                            "value": schema_search.DocumentSearchResponseFlat.ConfigDict.schema_extra["example"]
                        },
                        "grouped_response": {
                            "summary": "Response with (by_type=True)",
                            "value": schema_search.DocumentSearchResponseByType.ConfigDict.schema_extra["example"]
                        }
                    }
                }
            }
        },
        404: {
            "description": "Document not found on database",
            "content": {
                "application/json": {
                    "example": {"detail": "Document not found"}
                }
            }
        }
    }
)
async def search_on_document(
    search: schema_search.DocumentSearch,
    db: AsyncSession = Depends(get_async_db)
):
    document_obj = await repository_document.get_document_by_uuid(db, search.document_uuid)
    if not document_obj:
        raise HTTPException(status_code=404, detail="Document not found")
    
    labels = await repository_label.get_or_create(db, search.labels)
    
    return services_label.generate_relations_json(
        documents=document_obj.document,
        initial_labels=labels,
        by_type=search.by_type
    )
=======
    response = await service_document.create_or_update_documents(db, documents)
    return response


@router.delete("/", response_model=None)
async def delete_all(db: AsyncSession = Depends(get_async_db)):
    await service_document.delete_all(db)
    return {"detail": "All documents deleted"}
>>>>>>> 584054f2643d394146b28b1a7904c5d83a34115a
