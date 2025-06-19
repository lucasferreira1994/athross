from fastapi import FastAPI
from database import Base, engine
from api.routes import route_document, route_document_type, route_label

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Document API")

app.include_router(route_label.router)

app.include_router(route_document_type.router)

app.include_router(route_document.router)

