import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import Base, get_async_db
from main import app
from fastapi.testclient import TestClient

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Criando engine e sessionmaker para testes
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def override_get_async_db():
    async with TestSessionLocal() as session:
        yield session

app.dependency_overrides[get_async_db] = override_get_async_db

@pytest.fixture
def client():
    with TestClient(app, raise_server_exceptions=True) as c:
        yield c
