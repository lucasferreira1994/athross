from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import api.schemas.schema_document as schema_document
import repository.repository_document as repository_document
from factory.factory_database import get_async_db

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
    """
    Retrieve all documents from the database.

    Returns:
    List[Document]: A list containing complete document objects with:
        - id: Unique document identifier
        - title: Document title
        - content: Document content
        - type_id: Associated document type ID
        - created_at: Timestamp of creation
        - updated_at: Timestamp of last update
    """
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
async def create(
    documents: List[schema_document.DocumentCreate],
    db: AsyncSession = Depends(get_async_db)
):
    """
    Create or update multiple documents in a single operation.

    Parameters:
    - **documents**: List of DocumentCreate objects containing:
        - title (str): Document title (required)
        - content (str): Document content (required)
        - type_id (UUID): Associated document type ID (required)
        - metadata (dict, optional): Additional document metadata

    Returns:
    List[Document]: Created or updated document objects with complete details including:
        - System-generated ID
        - Timestamps
        - Full document data

    Note:
    This is an upsert operation - existing documents with matching titles will be updated.
    """
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
async def delete_all(db: AsyncSession = Depends(get_async_db)):
    """
    WARNING: This will permanently delete ALL documents in the system.

    Security:
    - Should be protected with admin-level authentication
    - Consider adding confirmation step in production

    Returns:
    dict: Confirmation message with operation result
    """
    await repository_document.delete_all(db)
    return {"detail": "All documents deleted"}