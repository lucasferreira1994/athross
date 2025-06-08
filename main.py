from fastapi import FastAPI
from .database import Base, engine
from .routers import documents, labels, document_types

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Document API")

app.include_router(documents.router)
app.include_router(labels.router)
app.include_router(document_types.router)