from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
import models.model_label as model_label
import api.schemas.schema_label as schema_label

async def list_all(db: AsyncSession):
    result = await db.execute(
        select(model_label.Label).order_by(model_label.Label.key)
    )
    return result.scalars().all()

async def get_or_create(db: AsyncSession, labels: List[schema_label.LabelCreate]):
    input_keys = [label.key for label in labels]

    result = await db.execute(
        select(model_label.Label).where(model_label.Label.key.in_(input_keys))
    )
    existing_labels = result.scalars().all()
    existing_keys = {label.key for label in existing_labels}

    new_labels = []
    for label_data in labels:
        if label_data.key not in existing_keys:
            new_label = model_label.Label(key=label_data.key, value=label_data.value)
            db.add(new_label)
            new_labels.append(new_label)

    if new_labels:
        await db.commit()
        for label in new_labels:
            await db.refresh(label)

    return existing_labels + new_labels

async def delete(db: AsyncSession, label_id: int):
    result = await db.execute(
        select(model_label.Label).where(model_label.Label.id == label_id)
    )
    existing_label = result.scalar_one_or_none()

    if not existing_label:
        raise HTTPException(status_code=404, detail="Label not found")

    await db.delete(existing_label)
    await db.commit()
    return existing_label
