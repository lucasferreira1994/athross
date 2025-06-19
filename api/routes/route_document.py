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
async def create(
    documents: List[schema_document.DocumentCreate],
    db: AsyncSession = Depends(get_async_db)
):
    response = await service_document.create_or_update_documents(db, documents)
    return response


@router.delete("/", response_model=None)
async def delete_all(db: AsyncSession = Depends(get_async_db)):
    await service_document.delete_all(db)
    return {"detail": "All documents deleted"}
