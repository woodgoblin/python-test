import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.main import app, get_db
from src.app.database import Base
import os
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# Create a new SQLite database for testing
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create the tables in the test database
Base.metadata.create_all(bind=engine)

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_create_cat(async_client):
    response = await async_client.post("/cats/", json={
        "birth_date": "2020-01-01",
        "paws_quantity": 4,
        "name": "Whiskers",
        "gender": "M",
        "tails_quantity": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Whiskers"

@pytest.mark.asyncio
async def test_read_cats(async_client):
    response = await async_client.get("/cats/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

@pytest.mark.asyncio
async def test_read_cat(async_client):
    response = await async_client.get("/cats/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Whiskers"

@pytest.mark.asyncio
async def test_update_cat(async_client):
    response = await async_client.put("/cats/1", json={
        "birth_date": "2020-01-01",
        "paws_quantity": 4,
        "name": "Whiskers Updated",
        "gender": "M",
        "tails_quantity": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Whiskers Updated"

@pytest.mark.asyncio
async def test_delete_cat(async_client):
    response = await async_client.delete("/cats/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Whiskers Updated"
