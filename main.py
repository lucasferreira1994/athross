from fastapi import FastAPI
from database import Base, engine
from api.routes import route_document, route_document_type, route_label, route_user
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Document API",
    description="Descricao a fazer",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(route_document.router)
app.include_router(route_document_type.router)
app.include_router(route_label.router)
app.include_router(route_user.router)
