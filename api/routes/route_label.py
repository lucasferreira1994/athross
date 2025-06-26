from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_async_db
import api.schemas.schema_label as schema_label
<<<<<<< HEAD
import repository.repository_label as repository_label

router = APIRouter(
    prefix="/labels",
    tags=["Labels"],
    responses={
        404: {"description": "Label not found"},
        422: {"description": "Validation error in request data"}
    }
)


@router.get(
    "/",
    response_model=List[schema_label.Label],
    summary="List all labels",
    description="Retrieves a list of all labels available in the system.",
    response_description="A list of label objects"
)
async def list_all(db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve all labels.

    Returns:
    List[Label]: A list containing all label objects with their details.
    """
    return await repository_label.list_all(db)


@router.post(
    "/",
    response_model=List[schema_label.Label],
    status_code=201,
    summary="Create new labels",
    description="Creates one or multiple new labels in the system. "
                "If a label already exists, returns the existing label.",
    response_description="List of created/existing label objects"
)
async def create(
    labels: List[schema_label.LabelCreate],
    db: AsyncSession = Depends(get_async_db)
):
    """
    Create new labels or get existing ones.

    Parameters:
    - **labels**: List of LabelCreate objects containing:
        - name (str): The name of the label (required, unique)
        - color (str, optional): Color code for the label

    Returns:
    List[Label]: List of label objects that were created or already existed.
    """
    return await repository_label.get_or_create(db, labels)


@router.patch(
    "/",
    response_model=List[schema_label.Label],
    summary="Update multiple labels",
    description="Updates one or multiple existing labels. "
                "Labels are matched by their names.",
    response_description="List of updated label objects"
)
async def update(
    labels: List[schema_label.LabelCreate],
    db: AsyncSession = Depends(get_async_db)
):
    """
    Update existing labels.

    Parameters:
    - **labels**: List of LabelCreate objects containing:
        - name (str): The name of the label to update (required)
        - color (str, optional): New color code for the label

    Returns:
    List[Label]: List of updated label objects.

    Raises:
    HTTPException 404: If any of the labels to update are not found
    """
    return await repository_label.patch(db, labels)


@router.delete(
    "/{label_id}",
    response_model=schema_label.Label,
    summary="Delete a label",
    description="Deletes a specific label by its unique identifier.",
    response_description="The deleted label object",
    responses={
        200: {"description": "Label successfully deleted"},
        404: {"description": "Label not found with the specified ID"}
    }
)
async def delete(
    label_id: UUID4,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Delete a label by ID.

    Parameters:
    - **label_id**: UUID4 - The unique identifier of the label to delete

    Returns:
    Label: The label object that was deleted.

    Raises:
    HTTPException 404: If no label exists with the specified ID
    """
    return await repository_label.delete(db, label_id)
=======
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
>>>>>>> 584054f2643d394146b28b1a7904c5d83a34115a
