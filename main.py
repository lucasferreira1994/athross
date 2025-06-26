from fastapi import FastAPI
from database import Base, engine
<<<<<<< HEAD
from api.routes import route_document, route_document_type, route_label, route_user

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Document API",
    description="Descricao a fazer",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.include_router(route_document.router)
app.include_router(route_document_type.router)
app.include_router(route_label.router)
app.include_router(route_user.router)
=======
from api.routes import route_document, route_document_type, route_label

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Document API")

app.include_router(route_label.router)

app.include_router(route_document_type.router)

app.include_router(route_document.router)

>>>>>>> 584054f2643d394146b28b1a7904c5d83a34115a
