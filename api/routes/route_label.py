from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_async_db
import api.schemas.schema_label as schema_label
import services.service_label as service_label

router = APIRouter(prefix="/api/v1/labels", tags=["labels"])


@router.get("/", response_model=List[schema_label.Label])
async def list_all(db: AsyncSession = Depends(get_async_db)):
    return await service_label.list_all(db)


@router.post("/", response_model=List[schema_label.Label])
async def create(labels: List[schema_label.LabelCreate], db: AsyncSession = Depends(get_async_db)):
    return await service_label.get_or_create(db, labels)


@router.patch("/", response_model=List[schema_label.Label])
async def update(labels: List[schema_label.LabelCreate], db: AsyncSession = Depends(get_async_db)):
    return await service_label.patch(db, labels)


@router.delete("/{label_id}", response_model=schema_label.Label)
async def delete(label_id: UUID4, db: AsyncSession = Depends(get_async_db)):
    return await service_label.delete(db, label_id)
